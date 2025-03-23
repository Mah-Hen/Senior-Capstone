import pandas as pd
import psycopg2
import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import numpy as np
import re

def initialize_db_connection():
    user = os.environ.get('USER')
    password = os.environ.get('PASS')
    host = os.environ.get('HOST')
    db = os.environ.get('DB')
    port = "5432"

    # Connect to the database
    uri = f"postgresql+psycopg2://{quote_plus(user)}:{quote_plus(password)}@{host}:{port}/{db}"
    print(uri)
    alchemyEngine = create_engine(uri)
    return alchemyEngine.connect()

def get_regions():
    # Northern Region
    north = [
        "Augusta", "Boston", "Concord", "Montpelier", "Albany", 
        "Hartford", "Providence", "Columbus", "Lansing", "Madison", 
        "Saint Paul", "Bismarck", "Pierre", "Helena"
    ]

    # Eastern Region
    east = [
        "Hartford", "Providence", "Boston", "Augusta", "Concord", 
        "Montpelier", "Albany", "Richmond", "Charleston", "Raleigh"
    ]

    # Southern Region
    south = [
        "Montgomery", "Little Rock", "Tallahassee", "Atlanta", 
        "Jackson", "Baton Rouge", "Columbia", "Nashville", "Austin", 
        "Oklahoma City", "Richmond", "Frankfort", "Charleston"
    ]

    # Western Region
    west = [
        "Phoenix", "Sacramento", "Denver", "Honolulu", "Boise", 
        "Jefferson City", "Carson City", "Santa Fe", "Salt Lake City", 
        "Olympia", "Cheyenne", "Salem", "Helena"
    ]

    return north,south, west, east


def main():
    db_connect = initialize_db_connection()
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    north, south, west, east = get_regions()
    # Read the data from the database
    q = """select l.layover_duration, a.airport_name, a.city
            from layovers l
            inner join Flight_features ff on l.flight_id=ff.flight_id
            inner join airports a on l.layover_airport_id=a.airport_id;"""
    for_fun_df = pd.read_sql(q, db_connect)    
    #print(for_fun_df.head())   

    q = """select ff.flight_price, ff.flight_direction, ff.num_stops, al.airline_name, ff.search_date, ad.airport_name, ad.city, ff.departure_time, ff.departure_date,
        aa.airport_name, aa.city, ff.arrival_time, ff.arrival_date, ff.travel_duration, ff.num_layovers, ff.num_carryon, ff.num_checked, ff.num_adults, ff.num_children, ff.num_infants_in_seat,
        ff.num_infants_on_lap, ff.seating_class, dplane.airplane_type, aplane.airplane_type
        from flight_features ff
        inner join airlines al on ff.airline_id=al.airline_id
        inner join airports ad on ff.departure_airport_id=ad.airport_id
        inner join airports aa on ff.arrival_airport_id =aa.airport_id
        inner join airplanes dplane on ff.departure_airplane_type_id=dplane.airplane_id 
        inner join airplanes aplane on ff.arrival_airplane_type_id=aplane.airplane_id;"""
    main_df = pd.read_sql(q, db_connect)    
    print(main_df.head()) 
    exit()
    # Filter the data based on the regions
    for_fun_df['Region'] = for_fun_df["city"].apply(lambda x: "North" if x in set(north) else "South" if x in set(south) else "West" if x in set(west) else "East")
    #print(for_fun_df.head())

    for_fun_df['hr'] = for_fun_df['layover_duration'].str.extract(r'(\d+) hr').fillna(0)
    for_fun_df['hr'] = for_fun_df['hr'].astype(int)
    for_fun_df['min'] = for_fun_df['layover_duration'].str.extract(r'(\d+) min').fillna(0)
    for_fun_df['min'] = for_fun_df['min'].astype(int)

    #print(for_fun_df[['layover_duration', 'hr', 'min']])

    for_fun_df["Duration_Label"] = np.where(
        for_fun_df["hr"] < 3, # Condition 1
         "Short", # Result 1
         np.where((for_fun_df["hr"].any() >= 3 & for_fun_df["hr"].any() < 6), # Condition 2
                "Medium", # Result 2
                np.where((for_fun_df["hr"].any() >= 6 & for_fun_df["hr"].any() < 12), # Condition 3
                         "Long", # Result 3
                         "Ultra-Long"
                )
        )
    )
    # Extract the hour and minute from the layover duration
    # Extract Day and Month from dates
    # Days between from Search Date and Departure Date
    # 
    #print(for_fun_df)

    #print(main_df.columns)

    year = "2025"
    main_df['hr'] = main_df['travel_duration'].str.extract(r'(\d+) hr').fillna(0)
    main_df['hr'] = main_df['hr'].astype(int)
    main_df['min'] = main_df['travel_duration'].str.extract(r'(\d+) min').fillna(0)
    main_df['min'] = main_df['min'].astype(int)

    for i in range(len(main_df["departure_date"])):
        duration_month = re.search(", (\\w+)", main_df["departure_date"][i])
        duration_month = duration_month.group().split(", ")[1]
        duration_month = months.index(duration_month) + 1
        duration_day = re.search("(\\d+)", main_df["departure_date"][i])
        duration_day = duration_day.group()
        main_df.loc[i, "departure_date"] = f"{duration_month}-{duration_day}-{year}"


    #print(main_df[['travel_duration', 'hr', 'min']])
    main_df['search_date'] = main_df['search_date'].astype('string')
    main_df['search_date'] = pd.to_datetime(main_df['search_date'])
    main_df["Search_Day"] = main_df["search_date"].dt.day
    main_df["Search_Month"] = main_df["search_date"].dt.month

    main_df['departure_date'] = pd.to_datetime(main_df['departure_date'])
    main_df["Departure_Day"] = main_df["departure_date"].dt.day
    main_df["Departure_Month"] = main_df["departure_date"].dt.month
    main_df["Days_Between"] = main_df["departure_date"] - main_df["search_date"]
    main_df["Days_Between"] = main_df["Days_Between"].dt.days
    #print(main_df[["search_date", "Search_Day", "Search_Month", "departure_date", "Departure_Day", "Departure_Month", "Days_Between"]])
    print(main_df.columns)
main()
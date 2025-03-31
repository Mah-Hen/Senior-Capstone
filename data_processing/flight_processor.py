import pandas as pd
import psycopg2
import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import numpy as np
import re


class FlightDataProcessor:
    def __init__(self):
        self.db_connect = self.initialize_db_connection()
        self.north, self.south, self.west, self.east = self.get_regions()
        self.months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        self._layover_df = None
        self._main_df = None
        self._user_df = None

    # the @Static method allows the method to be called without creating an instance of the class (i.e., without using self)
    @staticmethod
    def initialize_db_connection():
        user = os.environ.get("USER")
        password = os.environ.get("PASS")
        host = os.environ.get("HOST")
        db = os.environ.get("DB")
        port = "5432"

        # Connect to the database
        uri = f"postgresql+psycopg2://{quote_plus(user)}:{quote_plus(password)}@{host}:{port}/{db}"
        print(uri)
        alchemyEngine = create_engine(uri)
        return alchemyEngine.connect()

    @staticmethod
    def get_regions():
        # Northern Region
        north = [
            "Augusta",
            "Boston",
            "Concord",
            "Montpelier",
            "Albany",
            "Hartford",
            "Providence",
            "Columbus",
            "Lansing",
            "Madison",
            "Saint Paul",
            "Bismarck",
            "Pierre",
            "Helena",
        ]

        # Eastern Region
        east = [
            "Hartford",
            "Providence",
            "Boston",
            "Augusta",
            "Concord",
            "Montpelier",
            "Albany",
            "Richmond",
            "Charleston",
            "Raleigh",
        ]

        # Southern Region
        south = [
            "Montgomery",
            "Little Rock",
            "Tallahassee",
            "Atlanta",
            "Jackson",
            "Baton Rouge",
            "Columbia",
            "Nashville",
            "Austin",
            "Oklahoma City",
            "Richmond",
            "Frankfort",
            "Charleston",
        ]

        # Western Region
        west = [
            "Phoenix",
            "Sacramento",
            "Denver",
            "Honolulu",
            "Boise",
            "Jefferson City",
            "Carson City",
            "Santa Fe",
            "Salt Lake City",
            "Olympia",
            "Cheyenne",
            "Salem",
            "Helena",
        ]

        return north, south, west, east

    def fetch_layover_data(self):
        # Read the data from the database
        q = """select l.layover_duration, a.airport_name, a.city
                from layovers l
                inner join Flight_features ff on l.flight_id=ff.flight_id
                inner join airports a on l.layover_airport_id=a.airport_id;"""
        self._layover_df = pd.read_sql(q, self.db_connect)
        # print(for_fun_df.head())

    def process_layover_data(self):
        if self._layover_df is None:
            self.fetch_layover_data()

        # Add Region column
        self._layover_df["Layover_Region"] = self._layover_df["city"].apply(
            lambda x: (
                "North"
                if x in set(self.north)
                else (
                    "South"
                    if x in set(self.south)
                    else "West" if x in set(self.west) else "East"
                )
            )
        )

        # Parse duration components
        self._layover_df["Layover_Hour"] = (
            self._layover_df["layover_duration"].str.extract(r"(\d+) hr").fillna(0)
        )
        self._layover_df["Layover_Hour"] = self._layover_df["Layover_Hour"].astype(int)
        self._layover_df["Layover_Min"] = (
            self._layover_df["layover_duration"].str.extract(r"(\d+) min").fillna(0)
        )
        self._layover_df["Layover_Min"] = self._layover_df["mLayover_Minin"].astype(int)

        # Create duration labels
        self._layover_df["Layover_Duration_Label"] = np.where(
            (self._layover_df["Layover_Hour"] >= 3)
            & (self._layover_df["hLayover_Hourr"] < 6),
            "Medium",
            np.where(
                (self._layover_df["Layover_Hour"] >= 6)
                & (self._layover_df["Layover_Hour"] < 12),
                "Long",
                "Ultra-Long",
            ),
        )

    def fetch_main_data(self):
        # Read the data from the database
        q = """select ff.flight_price, ff.flight_direction, ff.num_stops, al.airline_name, ff.search_date, ad.airport_name AS departure_airport, ad.city AS departure_city, ff.departure_time, ff.departure_date,
            aa.airport_name AS arrival_airport, aa.city AS arrival_city, ff.arrival_time, ff.arrival_date, ff.travel_duration, ff.num_layovers, ff.num_carryon, ff.num_checked, ff.num_adults, ff.num_children, ff.num_infants_in_seat,
            ff.num_infants_on_lap, ff.seating_class, dplane.airplane_type AS departure_airplane_type, aplane.airplane_type AS arrival_airplane_type
            from flight_features ff
            inner join airlines al on ff.airline_id=al.airline_id
            inner join airports ad on ff.departure_airport_id=ad.airport_id
            inner join airports aa on ff.arrival_airport_id =aa.airport_id
            inner join airplanes dplane on ff.departure_airplane_type_id=dplane.airplane_id 
            inner join airplanes aplane on ff.arrival_airplane_type_id=aplane.airplane_id;"""
        self._main_df = pd.read_sql(q, self.db_connect)

    def process_main_data(self):
        if self._main_df is None:
            self.fetch_main_data()
        # Filter the data based on the regions

        # Extract the hour and minute from the layover duration
        self._main_df["Duration_Hour"] = (
            self._main_df["travel_duration"]
            .str.extract(r"(\d+) hr")
            .fillna(0)
            .astype(int)
        )
        self._main_df["Duration_Min"] = (
            self._main_df["travel_duration"]
            .str.extract(r"(\d+) min")
            .fillna(0)
            .astype(int)
        )
        # Extract Day and Month from dates
        self._main_df["search_date"] = pd.to_datetime(self._main_df["search_date"])
        departure_dates = self._main_df["departure_date"].str.extract(
            r", (?P<month>\w+) (?P<day>\d+)"
        )
        departure_dates["month"] = departure_dates["month"].map(
            lambda x: self.months.index(x) + 1
        )
        departure_dates["year"] = 2025
        self._main_df["departure_date"] = pd.to_datetime(
            departure_dates[["year", "month", "day"]]
        )
        # Days between from Search Date and Departure Date
        self._main_df["Days_Between"] = (
            self._main_df["departure_date"] - self._main_df["search_date"]
        ).dt.days

        # Add Travel Duration # Add Travel Duration Label
        self._main_df["Duration_Label"] = np.where(
            (self._main_df["Duration_Hour"] >= 3)
            & (self._main_df["Duration_Hour"] < 6),
            "Medium",
            np.where(
                (self._main_df["Duration_Hour"] >= 6)
                & (self._main_df["Duration_Hour"] < 12),
                "Long",
                "Ultra-Long",
            ),
        )  # Add Travel Duration Label
        self._main_df["Duration_Label"] = np.where(
            (self._main_df["Duration_Hour"] >= 3)
            & (self._main_df["Duration_Hour"] < 6),
            "Medium",
            np.where(
                (self._main_df["Duration_Hour"] >= 6)
                & (self._main_df["Duration_Hour"] < 12),
                "Long",
                "Ultra-Long",
            ),
        )
        self._main_df["Duration_Label"] = np.where(
            (self._main_df["Duration_Hour"] >= 3)
            & (self._main_df["Duration_Hour"] < 6),
            "Medium",
            np.where(
                (self._main_df["Duration_Hour"] >= 6)
                & (self._main_df["Duration_Hour"] < 12),
                "Long",
                "Ultra-Long",
            ),
        )

        # Add Layover Label
        self._main_df["Layover_Label"] = np.where(
            self._main_df["num_layovers"] == 0, "Direct", "Layover"
        )

        # Add Departure Morning/Afternoon/Evening/Night Flight
        self._main_df["Departure_Time"] = pd.to_datetime(
            self._main_df["departure_time"], format="%H:%M:%S"
        )
        self._main_df["Departure_Hour"] = self._main_df["Departure_Time"].dt.hour
        self._main_df["Departure_AMPM"] = np.where(
            self._main_df["Departure_Hour"] < 12, "AM", "PM"
        )
        self._main_df["Departure_Time_Label"] = np.where(
            (self._main_df["Departure_Hour"] >= 6)
            & (self._main_df["Departure_Hour"] < 12),
            "Morning",
            np.where(
                (self._main_df["Departure_Hour"] >= 12)
                & (self._main_df["Departure_Hour"] < 18),
                "Afternoon",
                np.where(
                    (self._main_df["Departure_Hour"] >= 18)
                    & (self._main_df["Departure_Hour"] < 24),
                    "Evening",
                    "Night",
                ),
            ),
        )

        # Add Arrival Morning/Afternoon/Evening/Night Flight
        self._main_df["Arrival_Time"] = pd.to_datetime(
            self._main_df["arrival_time"], format="%H:%M:%S"
        )
        self._main_df["Arrival_Hour"] = self._main_df["Arrival_Time"].dt.hour
        self._main_df["Arrival_AMPM"] = np.where(
            self._main_df["Arrival_Hour"] < 12, "AM", "PM"
        )
        self._main_df["Arrival_Time_Label"] = np.where(
            (self._main_df["Arrival_Hour"] >= 6) & (self._main_df["Arrival_Hour"] < 12),
            "Morning",
            np.where(
                (self._main_df["Arrival_Hour"] >= 12)
                & (self._main_df["Arrival_Hour"] < 17),
                "Afternoon",
                np.where(
                    (self._main_df["Arrival_Hour"] >= 17)
                    & (self._main_df["Arrival_Hour"] < 21),
                    "Evening",
                    "Night",
                ),
            ),
        )

        # Extract extra time components
        self._main_df["Search_Day"] = self._main_df["search_date"].dt.day
        self._main_df["Search_Month"] = self._main_df["search_date"].dt.month
        self._main_df["Departure_Day"] = self._main_df["departure_date"].dt.day
        self._main_df["Departure_Month"] = self._main_df["departure_date"].dt.month
        self._main_df["arrival_date"] = self._main_df["arrival_date"].astype("string")
        self._main_df["Arrival_Day"] = self._main_df["arrival_date"].str.extract(
            r"\w+ (\d+)"
        )
        self._main_df["Arrival_Month"] = (
            self._main_df["arrival_date"]
            .str.extract(r", (\w+)")
            .map(lambda x: self.months.index(x) + 1)
        )

        # Add Region column
        self._main_df["Departure_Region"] = self._main_df["departure_city"].apply(
            lambda x: (
                "North"
                if x in set(self.north)
                else (
                    "South"
                    if x in set(self.south)
                    else "West" if x in set(self.west) else "East"
                )
            )
        )
        self._main_df["Arrival_Region"] = self._main_df["arrival_city"].apply(
            lambda x: (
                "North"
                if x in set(self.north)
                else (
                    "South"
                    if x in set(self.south)
                    else "West" if x in set(self.west) else "East"
                )
            )
        )

        # Add Season column
        self._main_df["Departure_Season"] = self._main_df["Departure_Month"].apply(
            lambda x: (
                "Winter"
                if x in [12, 1, 2]
                else (
                    "Spring"
                    if x in [3, 4, 5]
                    else "Summer" if x in [6, 7, 8] else "Fall"
                )
            )
        )
        self._main_df["Arrival_Season"] = self._main_df["Arrival_Month"].apply(
            lambda x: (
                "Winter"
                if x in [12, 1, 2]
                else (
                    "Spring"
                    if x in [3, 4, 5]
                    else "Summer" if x in [6, 7, 8] else "Fall"
                )
            )
        )

        self._main_df["seating_class"] = self._main_df["seating_class"]
        vals = ["1", "0", "Unknown"]
        self._main_df["airline_name"] = self._main_df["airline_name"][
            self._main_df.airline_name.isin(vals) == False
        ]

        self._main_df["departure_airport"] = self._main_df["departure_airport"][
            self._main_df.departure_airport.isin(["0", "2"]) == False
        ]
        self._main_df = self._main_df.dropna(subset=["departure_airport"])

    def process_user_data(self, dict):
        # Extract the hour and minute from the layover duration
        self._main_df["Duration_Hour"] = (
            self._main_df["travel_duration"]
            .str.extract(r"(\d+) hr")
            .fillna(0)
            .astype(int)
        )
        self._main_df["Duration_Min"] = (
            self._main_df["travel_duration"]
            .str.extract(r"(\d+) min")
            .fillna(0)
            .astype(int)
        )
        # Extract Day and Month from dates
        self._main_df["search_date"] = pd.to_datetime(self._main_df["search_date"])
        departure_dates = self._main_df["departure_date"].str.extract(
            r", (?P<month>\w+) (?P<day>\d+)"
        )
        departure_dates["month"] = departure_dates["month"].map(
            lambda x: self.months.index(x) + 1
        )
        departure_dates["year"] = 2025
        self._main_df["departure_date"] = pd.to_datetime(
            departure_dates[["year", "month", "day"]]
        )
        # Days between from Search Date and Departure Date
        self._main_df["Days_Between"] = (
            self._main_df["departure_date"] - self._main_df["search_date"]
        ).dt.days

        # Add Travel Duration # Add Travel Duration Label
        self._main_df["Duration_Label"] = np.where(
            (self._main_df["Duration_Hour"] >= 3)
            & (self._main_df["Duration_Hour"] < 6),
            "Medium",
            np.where(
                (self._main_df["Duration_Hour"] >= 6)
                & (self._main_df["Duration_Hour"] < 12),
                "Long",
                "Ultra-Long",
            ),
        )  # Add Travel Duration Label
        self._main_df["Duration_Label"] = np.where(
            (self._main_df["Duration_Hour"] >= 3)
            & (self._main_df["Duration_Hour"] < 6),
            "Medium",
            np.where(
                (self._main_df["Duration_Hour"] >= 6)
                & (self._main_df["Duration_Hour"] < 12),
                "Long",
                "Ultra-Long",
            ),
        )
        self._main_df["Duration_Label"] = np.where(
            (self._main_df["Duration_Hour"] >= 3)
            & (self._main_df["Duration_Hour"] < 6),
            "Medium",
            np.where(
                (self._main_df["Duration_Hour"] >= 6)
                & (self._main_df["Duration_Hour"] < 12),
                "Long",
                "Ultra-Long",
            ),
        )

        # Add Layover Label
        self._main_df["Layover_Label"] = np.where(
            self._main_df["num_layovers"] == 0, "Direct", "Layover"
        )

        # Add Departure Morning/Afternoon/Evening/Night Flight
        self._main_df["Departure_Time"] = pd.to_datetime(
            self._main_df["departure_time"], format="%H:%M:%S"
        )
        self._main_df["Departure_Hour"] = self._main_df["Departure_Time"].dt.hour
        self._main_df["Departure_AMPM"] = np.where(
            self._main_df["Departure_Hour"] < 12, "AM", "PM"
        )
        self._main_df["Departure_Time_Label"] = np.where(
            (self._main_df["Departure_Hour"] >= 6)
            & (self._main_df["Departure_Hour"] < 12),
            "Morning",
            np.where(
                (self._main_df["Departure_Hour"] >= 12)
                & (self._main_df["Departure_Hour"] < 18),
                "Afternoon",
                np.where(
                    (self._main_df["Departure_Hour"] >= 18)
                    & (self._main_df["Departure_Hour"] < 24),
                    "Evening",
                    "Night",
                ),
            ),
        )

        # Add Arrival Morning/Afternoon/Evening/Night Flight
        self._main_df["Arrival_Time"] = pd.to_datetime(
            self._main_df["arrival_time"], format="%H:%M:%S"
        )
        self._main_df["Arrival_Hour"] = self._main_df["Arrival_Time"].dt.hour
        self._main_df["Arrival_AMPM"] = np.where(
            self._main_df["Arrival_Hour"] < 12, "AM", "PM"
        )
        self._main_df["Arrival_Time_Label"] = np.where(
            (self._main_df["Arrival_Hour"] >= 6) & (self._main_df["Arrival_Hour"] < 12),
            "Morning",
            np.where(
                (self._main_df["Arrival_Hour"] >= 12)
                & (self._main_df["Arrival_Hour"] < 17),
                "Afternoon",
                np.where(
                    (self._main_df["Arrival_Hour"] >= 17)
                    & (self._main_df["Arrival_Hour"] < 21),
                    "Evening",
                    "Night",
                ),
            ),
        )

        # Extract extra time components
        self._main_df["Search_Day"] = self._main_df["search_date"].dt.day
        self._main_df["Search_Month"] = self._main_df["search_date"].dt.month
        self._main_df["Departure_Day"] = self._main_df["departure_date"].dt.day
        self._main_df["Departure_Month"] = self._main_df["departure_date"].dt.month
        self._main_df["arrival_date"] = self._main_df["arrival_date"].astype("string")
        self._main_df["Arrival_Day"] = self._main_df["arrival_date"].str.extract(
            r"\w+ (\d+)"
        )
        self._main_df["Arrival_Month"] = (
            self._main_df["arrival_date"]
            .str.extract(r", (\w+)")
            .map(lambda x: self.months.index(x) + 1)
        )

        # Add Region column
        self._main_df["Departure_Region"] = self._main_df["departure_city"].apply(
            lambda x: (
                "North"
                if x in set(self.north)
                else (
                    "South"
                    if x in set(self.south)
                    else "West" if x in set(self.west) else "East"
                )
            )
        )
        self._main_df["Arrival_Region"] = self._main_df["arrival_city"].apply(
            lambda x: (
                "North"
                if x in set(self.north)
                else (
                    "South"
                    if x in set(self.south)
                    else "West" if x in set(self.west) else "East"
                )
            )
        )

        # Add Season column
        self._main_df["Departure_Season"] = self._main_df["Departure_Month"].apply(
            lambda x: (
                "Winter"
                if x in [12, 1, 2]
                else (
                    "Spring"
                    if x in [3, 4, 5]
                    else "Summer" if x in [6, 7, 8] else "Fall"
                )
            )
        )
        self._main_df["Arrival_Season"] = self._main_df["Arrival_Month"].apply(
            lambda x: (
                "Winter"
                if x in [12, 1, 2]
                else (
                    "Spring"
                    if x in [3, 4, 5]
                    else "Summer" if x in [6, 7, 8] else "Fall"
                )
            )
        )

        self._main_df["seating_class"] = self._main_df["seating_class"]
        vals = ["1", "0", "Unknown"]
        self._main_df["airline_name"] = self._main_df["airline_name"][
            self._main_df.airline_name.isin(vals) == False
        ]

        self._main_df["departure_airport"] = self._main_df["departure_airport"][
            self._main_df.departure_airport.isin(["0", "2"]) == False
        ]
        self._main_df = self._main_df.dropna(subset=["departure_airport"])

    def get_processed_layover_data(self):
        if self._layover_df is None:
            self.process_layover_data()
        return self._layover_df

    def get_processed_main_data(self):
        if self._main_df is None:
            self.process_main_data()
        return self._main_df

    def get_processed_user_data(self):
        if self._user_df is None:
            self.process_user_data()
        return self._user_df


if __name__ == "__main__":
    data = FlightDataProcessor()
    data = data.get_processed_user_data()

    print(data.columns)

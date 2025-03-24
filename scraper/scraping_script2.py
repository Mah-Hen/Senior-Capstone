from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import spacy
from spacy.matcher import Matcher 
import re 
import psycopg2
from datetime import datetime
import os
import logging



#URL = "https://www.google.com/travel/explore"

def intialize(URL):
    '''Open Google Flights Explore page'''
    # Create a new instance of the Chrome browser using Selenium's WebDriver
    driver = webdriver.Chrome()

    # Go to Google Flights Explore page
    driver.get(URL)

    # Pause execution of code for 2 seconds to allow the page to load fully
    time.sleep(2)

    # Initialize WebDriverWait object to wait for elements on the page for 5 seconds
    wait = WebDriverWait(driver, 5)

    # Return both driver and wait objects for further interactions with the page
    return driver, wait

def intializeDatabase():
    user = os.environ.get('USER')
    password = os.environ.get('PASS')
    host = os.environ.get('HOST')
    db = os.environ.get('DB')
    port = "5432"
    '''Initialize the database'''
    conn = psycopg2.connect(
        host=host,
        database=db,
        user=user,
        password=password,
        port = port
    )
    return conn, conn.cursor()

def closeConnection(conn, cursor):
    conn.close()
    cursor.close()
    
def accessTripLength(wait):
    '''Trip-Length'''
    # Find the Trip-Length button
    trip_length_button = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "div[jsname='S55YWb']"))) 
    
    # Click the Trip-Length button
    trip_length_button.click() 
    
    # Pause Execution of code for 2 seconds
    time.sleep(2) 
    
def accessSpecificDates(wait, driver, departure_date, return_date):
    accessTripLength(wait)
    '''Specific Dates'''
    #Click Specific Dates Button
    specific_dates_button = driver.find_element(By.CSS_SELECTOR, "div[jsname='mAKh3e']").find_element(By.CSS_SELECTOR, "button[id='sNlbpb']")
    
    # Click the Specific Dates button
    specific_dates_button.click()
    time.sleep(2)
    
    # Find the Departure Date input field
    departure_date_input = driver.find_element(By.CSS_SELECTOR, "div[jsname='O3Z1Eb']").find_element(By.CSS_SELECTOR, "input[aria-label='Departure']")
    departure_date_input.click()
    time.sleep(1)
    
    # Enter the Departure Date
    departure_date_input.send_keys(departure_date) # 1/5/2025 is just a placeholder date
    time.sleep(2)
    
    # Find the Return Date input field
    departure_date_input = driver.find_element(By.CSS_SELECTOR, "div[jsname='O3Z1Eb']").find_element(By.CSS_SELECTOR, "input[aria-label='Return']")
    departure_date_input.click()
    departure_date_input.send_keys(return_date)
    time.sleep(1)
    departure_date_input.send_keys(Keys.ENTER)
    time.sleep(5)
    
    # Click Done Button
    # Wait for the Done button to appear
    div = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='ohKsQc']")))
    done_button = div.find_element(By.CSS_SELECTOR, "button[jsname='McfNlf']")
    done_button.click() 
    time.sleep(2) 
    
    
def accessFlexibleDates(wait, driver, month, week_type):
    '''Flexible Dates'''
    #accessTripLength(wait) # Access Trip-Length entry-button for user
    accessTripLength(wait)
    current_month = datetime.now().month
    print(current_month) 
    button_number = month-current_month
    try: 
        if month == "all":
            all_months_button = driver.find_element(By.CSS_SELECTOR, "span[data-value='0']").find_element(By.CSS_SELECTOR, "button[jsname='LgbsSe']")
            all_months_button.click()
            time.sleep(1)
    except:
        month_button = driver.find_element(By.CSS_SELECTOR, f"span[data-value='{button_number+1}']").find_element(By.CSS_SELECTOR, "button[jsname='LgbsSe']")
        month_button.click
    

    #span_text = "2 weeks"  # You can change this to any text you're looking for regarding trip duration (Weekend, 1 week, 2 weeks)
    # Find the span element with the text of the week_type
    trip_duration_div = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Trip duration']")   
    span = trip_duration_div.find_element(By.XPATH, f".//span[normalize-space(text())='{week_type}']") # span_text
    
    # Access the button element
    button = span.find_element(By.XPATH, "..//..//..//..//button")
    button.click()
    
    #Click Done Button
    div = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='ohKsQc']")))
    done_button = div.find_element(By.CSS_SELECTOR, "button[jsname='McfNlf']")
    done_button.click() 
    time.sleep(2) 
    

def accessNumOfPassengers(wait, driver, num_adults, num_children, num_infants_in_seat, num_infants_on_lap):
    '''Retreieve the # of passangers'''
    
    # Number of people going
    # access the number of passengers button
    
    num_of_passengers_button = driver.find_element(By.CSS_SELECTOR, "div[jsname='QqIbod']")
    num_of_passengers_button.click()
    time.sleep(2)
    
    # access the add adult button
    if num_adults > 1:
        add_adult_button = driver.find_element(By.CSS_SELECTOR, "ul[jsname='nK2kYb']").find_element(By.CSS_SELECTOR, "button[aria-label='Add adult']")
        for i in range(num_adults-1):
            add_adult_button.click()
            time.sleep(1)
    
    # access the add children button
    if num_children > 0:
        add_children_button = driver.find_element(By.CSS_SELECTOR, "ul[jsname='nK2kYb']").find_element(By.CSS_SELECTOR, "button[aria-label='Add child']")
        for i in range(num_children):
            add_children_button.click()
            time.sleep(1)
    
    # access the add infants in seat button
    if num_infants_in_seat > 0:
        add_infants_in_seat_button = driver.find_element(By.CSS_SELECTOR, "ul[jsname='nK2kYb']").find_element(By.CSS_SELECTOR, "button[aria-label='Add infant in seat'")
        for i in range(num_infants_in_seat):
            add_infants_in_seat_button.click()
            time.sleep(1)
    
    # access the add infants on lap button
    if num_infants_on_lap > 0:
        add_infants_on_lap_button = driver.find_element(By.CSS_SELECTOR, "ul[jsname='nK2kYb']").find_element(By.CSS_SELECTOR, "button[aria-label=aria-label='Add infant on lap']")
        for i in range(num_infants_on_lap):
            add_infants_on_lap_button.click()
            time.sleep(1)
    time.sleep(1)
    

def accessSeatingClass(wait, driver, class_type):
    ''' Retrive the Seating Class (Economy, Prem Econ, Business, First Class) '''
    
    # access the seating class button
    seating_class_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div[jsname='zkxPxd']")))
    seating_class_button.click()
    time.sleep(1)
    if class_type.lower() == "Economy".lower():
        class_type_button = driver.find_element(By.CSS_SELECTOR, "ul[aria-label='Select your preferred seating class.']").find_element(By.CSS_SELECTOR, "li[data-value='1']") # 1 = Economy, 2 = Prem Econ, 3 = Business, 4 = First
        class_type_button.click()
    if class_type.lower() == "Prem Econ".lower():
        class_type_button = driver.find_element(By.CSS_SELECTOR, "ul[aria-label='Select your preferred seating class.']").find_element(By.CSS_SELECTOR, "li[data-value='2']") # 1 = Economy, 2 = Prem Econ, 3 = Business, 4 = First
        class_type_button.click()
    if class_type.lower() == "Business".lower():
        class_type_button = driver.find_element(By.CSS_SELECTOR, "ul[aria-label='Select your preferred seating class.']").find_element(By.CSS_SELECTOR, "li[data-value='3']") # 1 = Economy, 2 = Prem Econ, 3 = Business, 4 = First
        class_type_button.click()
    if class_type.lower() == "First Class".lower():
        class_type_button = driver.find_element(By.CSS_SELECTOR, "ul[aria-label='Select your preferred seating class.']").find_element(By.CSS_SELECTOR, "li[data-value='4']") # 1 = Economy, 2 = Prem Econ, 3 = Business, 4 = First
        class_type_button.click()
    time.sleep(2)
    
def changeRoundTrip(wait, driver, roundtrip):
    ''' Retrive Round Trip or One way '''
    #Click Round-Trip Button
    if not roundtrip:
        round_trip_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div[jsname='L3XY7b']")))
        round_trip_button.click()
        time.sleep(2)
    
        # Change to One-Way
        ticket_type = driver.find_element(By.CSS_SELECTOR, "ul[aria-label='Select your ticket type.']").find_element(By.CSS_SELECTOR, "li[data-value='2']") # data-value = '1' gives round trip else one-way
        ticket_type.click()
        time.sleep(2)
    
def accessOriginDestination(wait, driver, origin, destination):
    '''Retrieve Origin and Destination'''
    
    #Retrieve Origin input field
    element = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Where from?"]')
    element.clear()
    element.send_keys(origin+"") # Send keys to the input field
    time.sleep(2)
    #Retrieve the dropdown list
    dropdown = wait.until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, "ul[role='listbox'].DFGgtd")
    ))
    option = dropdown.find_element(By.CSS_SELECTOR, "li[role='option']")
    option.click()
    time.sleep(2.5)


    #Retrieve Destination input field
    dest_input = driver.find_element(By.CSS_SELECTOR, "input[aria-label='Where to?']")
    dest_input.clear()
    dest_input.send_keys(destination+"") 
    
    #Retrieve the dropdown list
    dropdown = wait.until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, "ul[role='listbox'].DFGgtd")
    ))
    option = dropdown.find_element(By.CSS_SELECTOR, "li[role='option']")
    option.click()
    time.sleep(2)
    
def access_Flights(driver):
    '''Retrieve Flights'''
    # Find the View Flights link
    view_flights_link = driver.find_element(By.CSS_SELECTOR, "a[aria-label='View flights']")
    new_URL = view_flights_link.get_attribute("href")
    #view_flights_link.click()
    # Retrieve the new URL (GoogleFlights/flights page)
    driver.get(new_URL)
    time.sleep(2)
    
    '''View More Flights'''
    view_more_flights_button = driver.find_element(By.XPATH, "//button[@aria-label='View more flights']")
    driver.find_element(By.TAG_NAME, "Body").send_keys(Keys.HOME)
    view_more_flights_button.click()
    time.sleep(2)
    # Scroll the element into view using JavaScript so we can click on the button
    driver.find_element(By.TAG_NAME, "Body").send_keys(Keys.HOME) #driver.execute_script("arguments[0].scrollIntoView(true);", view_more_flights_button)
    time.sleep(1)
    
def retrieveFlightDetails(driver, wait, round_trip):
    #Flight Details    
    all_results = driver.find_elements(By.XPATH, "//ul[@class='Rk10dc']/li")
    flight_info = []
    cnt = 0
    
    for result in all_results[:25]:
        dropdown_button = None
        tuple_dict = {}
        wait.until(EC.visibility_of_element_located((By.XPATH, ".//div[@class='JMc5Xc']")))
        try:
            aria_label = result.find_element(By.XPATH, ".//div[@class='JMc5Xc']").get_attribute("aria-label")#.find_element(By.CSS_SELECTOR, "div[@class='JMc5Xc']").get_attribute("aria-label") #result.find_element(By.CSS_SELECTOR, ".//div[@class='JMc5Xc']").get_attribute("aria-label") 
        except:
             break
        if aria_label:
            cnt += 1
            print(aria_label + "\n")
            aria_label = aria_label.replace("\u202f", " ")
            # Call NLP function to extract flight information
            #Airplane Type
            '''Throw a Selenium Wait Here'''
            dropdown_button = result.find_element(By.CSS_SELECTOR, "div[jsname='UsVyAb']").find_element(By.CSS_SELECTOR, "button[jsname='LgbsSe']")#.find_element(By.XPATH, "//Button[jsname='LgbsSe']")
            driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_button)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[jsname='LgbsSe']"))) #VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-Bz112c-M1Soyc VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe LQeN7 nJawce OTelKf XPGpHc mAozAc   # Check if the element is enabled 
            driver.execute_script("arguments[0].click();", dropdown_button)
            #dropdown_button.click()
            driver.execute_script("window.scrollBy(0,-100);")
            
            time.sleep(2)
            # Annoying ass error here
            try:
                super_div_element = div_element = result.find_element(By.CSS_SELECTOR, 'div.m9ravf').find_element(By.CSS_SELECTOR, 'div.xOMPfb.MNvMJb')
                
                div_element = super_div_element.find_element(By.CSS_SELECTOR, "div.c257Jb.QwxBBf.eWArhb") 
                span_elements = div_element.find_elements(By.CSS_SELECTOR,"span.Xsgmwe")
                departure_airplane_type = span_elements[3].text

                div_element = super_div_element.find_element(By.CSS_SELECTOR, "div.MX5RWe.sSHqwe.y52p7d")
                span_elements = div_element.find_elements(By.CSS_SELECTOR,"span.Xsgmwe")
                arrival_airplane_type = span_elements[3].text
                dropdown_button.click()
                
                tuple_dict["Departure Airplane Type"] = departure_airplane_type
                tuple_dict["Arrival Airplane Type"] = arrival_airplane_type
                #tuple_dict[""] = arrival_airplane_type
            except:
                print()
                
            doc = nlp(aria_label)
            for token in doc:
                print(f"Token: {token.text}, Lemma: {token.lemma_}, POS: {token.pos_}, Tag: {token.tag_}, Dep: {token.dep_}, Shape: {token.shape_}, is_alpha: {token.is_alpha}, is_stop: {token.is_stop}")
            tuple_dict["One-Way Info"] = extractFlightInfo(doc)
            
            
            
            '''Round Trip'''
            if round_trip:
                prev_url = driver.current_url
                cnt = 0
                while True:
                    # Error here
                    try:
                        all_results = driver.find_elements(By.XPATH, "//ul[@class='Rk10dc']/li")
                        select_flight = all_results[cnt].find_element(By.XPATH, ".//div[@class='gQ6yfe m7VU8c']")
                        select_flight.click()
                    except:
                        break
                    try:
                        view_more_flights = driver.find_element(By.XPATH, ".//div[@jsname='YdtKid']").find_element(By.XPATH, ".//button[@jsname='ornU0b']")
                        view_more_flights.click()
                    except:
                        print("")
                        
                    time.sleep(2)
                    more_results = driver.find_elements(By.XPATH, "//ul[@class='Rk10dc']/li")
                    randomHash = {}
                    for more_result in more_results:
                        try:
                            aria_label = more_result.find_element(By.XPATH, ".//div[@class='JMc5Xc']").get_attribute("aria-label")
                        except:
                            break
                        if aria_label is not None:
                            doc = nlp(aria_label)
                            print(aria_label + "\n")
                            tuple_dict["Round-Trip Info"] = extractFlightInfo(doc)
                        time.sleep(2)
                        
                    cnt += 1
                    driver.get(prev_url)
                    #all_results = driver.find_elements(By.XPATH, "//ul[@class='Rk10dc']/li")
                    
            flight_info.append(tuple_dict)
                    
    return flight_info


    
def retrieveAirplaneType(driver):
    all_results = driver.find_elements(By.XPATH, "//ul[@class='Rk10dc']/li")
    for result in all_results:
        dropdown_button = result.find_element(By.CSS_SELECTOR, "div[jsname='UsVyAb']").find_element(By.CSS_SELECTOR, "button[jsname='LgbsSe']")#.find_element(By.XPATH, "//Button[jsname='LgbsSe']")
        dropdown_button.click()
        time.sleep(2)
        div_element = result.find_element(By.CSS_SELECTOR, "div[jsname='XxAJue']").find_element(By.CSS_SELECTOR, "div[jsname='lVbzR']")
        div_element = div_element.find_element(By.CSS_SELECTOR, "div.MX5RWe.sSHqwe.y52p7d")
        span_elements = div_element.find_elements(By.CSS_SELECTOR,"span.Xsgmwe")
        airplane_type = span_elements[3].text
        return airplane_type


    
    
def extractFlightInfo(nlp_doc):
    '''Extracting flight information using spacy's NLP'''
    '''The hardest part really. Took a couple weeks to get this right'''
    extracted = []
    price_pattern = [
        [{"POS": "NUM"}, {"ORTH": "US"}, {"ORTH": "dollars"}] 
        ]
    num_stops_pattern = [
        [{"POS": "NUM"}, {"LEMMA": "stop"}, {"LOWER": "flight"}]
    ]
    
    no_stops_pattern = [
     [{"LOWER": "nonstop"}]   
    ]
    
    duration_pattern = [
         [{"TEXT": "Total"}, {"TEXT": "duration"}, {"POS": "NUM"}, {"LOWER": "hr"}, {"POS": "NUM", "OP":"?"}, {"LOWER": "min", "OP":"?"}],
         [{"TEXT": "Total"}, {"TEXT": "duration"}, {"POS": "NUM"}, {"LOWER": "min", "OP":"?"}],
    ]
    '''May need to change later'''
    num_layover_pattern = [
        [{"TEXT": "of"}, {"POS": "NUM"}, {"TEXT": ")"}]
    ]
    
    '''
    layover_duration_pattern = [
        [{"POS": "NUM"}, {"LOWER": "hr"}, {"POS": "NUM"}, {"LOWER": "min"}, {"LOWER": "layover"}], 
        [{"POS": "NUM"}, {"LOWER": "min"}, {"LOWER", "layover"}], 
        [{"POS":"NUM"}, {"LOWER": "hr"}, {"LOWER": "overnight", "POS":"?"}, {"LOWER": "layover"}]
    ]
    '''
    
    departure_time_pattern = [
        [
        {"TEXT": "Leaves"}, {"POS": "PROPN", "OP": "+"}, {"POS": {"IN": ["SYM", "PUNCT", "CCONJ"]}, "OP": "?"}, {"POS": "PROPN", "OP": "+"}, {"TEXT": "Airport"},
        {"LOWER": "at"}, {"POS": "NUM"}, {"IS_SPACE": True, "OP": "*"}, {"LOWER": {"IN": ["am", "pm"]}},
        {"LOWER": "on"}, {"POS": "PROPN"}, {"TEXT": ","},
        {"POS": "PROPN"},{"POS": "NUM"},
        ]
    ]
    
    arrival_time_pattern = [
       [{"TEXT":"arrives"}, {"LOWER":"at"}, {"POS": "PROPN", "OP": "+"},
        {"POS": {"IN": ["SYM", "PUNCT", "CCONJ"]}, "OP": "?"}, {"POS": "PROPN", "OP": "?"}, {"TEXT": "Airport"}, {"LOWER":"at"}, {"POS": "NUM"}, {"IS_SPACE": True, "OP": "*"}, 
        {"LOWER": {"IN": ["am", "pm"]}}, {"LOWER": "on"}, {"POS": "PROPN"}, {"TEXT": ","}, {"POS":"PROPN"}, {"POS": "NUM"}],
       [{"TEXT":"arrives"},{"LOWER":"at"}, {"POS":"PROPN", "OP":"+"}, {"POS":{"IN":["SYM", "PUNCT", "CCONJ"]}, "OP":"?"}, {"POS":"PROPN", "OP":"+"}, {"TEXT":"Airport"}, {"POS":"PUNCT", "OP":"?"}, {"POS":"PROPN", "OP":"?"}, {"POS":"PUNCT", "OP":"?"}, {"LOWER":"at"}, {"POS": "NUM"}, {"IS_SPACE": True, "OP": "*"},
        {"LOWER": {"IN": ["am", "pm"]}}, {"LOWER": "on"}, {"POS": "PROPN"}, {"TEXT": ","}, {"POS":"PROPN"}, {"POS": "NUM"}
        ], 
         [{"TEXT":"arrives"},{"LOWER":"at"}, {"POS":"PROPN", "OP":"+"}, {"POS":{"IN":["SYM", "PUNCT", "CCONJ"]}, "OP":"?"}, {"POS":"PROPN", "OP":"+"}, {"TEXT":"Sunport"}, {"POS":"PUNCT", "OP":"?"}, {"POS":"PROPN", "OP":"?"}, {"POS":"PUNCT", "OP":"?"}, {"LOWER":"at"}, {"POS": "NUM"}, {"IS_SPACE": True, "OP": "*"},
        {"LOWER": {"IN": ["am", "pm"]}}, {"LOWER": "on"}, {"POS": "PROPN"}, {"TEXT": ","}, {"POS":"PROPN"}, {"POS": "NUM"}
        ]
       ]
    
    arrival_time_pattern_2 = [
       [{"TEXT":"arrives"},{"LOWER":"at"}, {"POS":"PROPN", "OP":"+"}, {"POS":{"IN":["SYM", "PUNCT", "CCONJ"]}, "OP":"?"}, {"POS":"PROPN", "OP":"+"}, {"TEXT":"Airport"}, {"POS":"PUNCT", "OP":"?"}, {"POS":"PROPN", "OP":"?"}, {"POS":"PUNCT", "OP":"?"}, {"LOWER":"at"}, {"POS": "NUM"}, {"IS_SPACE": True, "OP": "*"},
        {"LOWER": {"IN": ["am", "pm"]}}, {"LOWER": "on"}, {"POS": "PROPN"}, {"TEXT": ","}, {"POS":"PROPN"}, {"POS": "NUM"}
        ]
       ]
    
    layover_duration_pattern = [
        [{"LOWER":"is"}, {"LOWER":"a"}, {"POS": "NUM"}, {"LOWER": "hr"}, {"POS": "NUM", "OP":"+"}, {"LOWER": "min", "OP":"+"}]
    ]
    
    layover_duration_pattern_2 = [
        [{"LOWER":"is"}, {"LOWER":"a"}, {"POS": "NUM"}, {"LOWER": "min"}]
    ]
    
    layover_duration_pattern_3 = [
        [{"LOWER":"is"}, {"LOWER":"a"}, {"POS": "NUM"}, {"LOWER": "hr"}, {"lower":"overnight", "OP": "?"}, {"LOWER":"layover"}]
    ]
    
    airline_pattern = [ 
        [{"LOWER": "with"}, {"POS": "PROPN"}], 
        [{"LOWER": "with"}, {"POS": {"IN": ["ADJ", "PROPN"]}}, {"POS": "CCONJ", "OP":"?"}, {"POS": "PROPN"}]
    ]
    connecting_airport_pattern = [
        [{"LOWER":"layover"}, {"LOWER": "at"}, {"POS":"PROPN", "OP":"+"},{"POS":{"IN":["PUNCT", "SYM", "CCONJ"]}, "OP":"?"}, 
         {"POS":"PROPN", "OP":"*"}, {"TEXT": "Airport"}, {"LOWER": "in"}, {"POS": "PROPN", "OP":"+"}], 

        [{"LOWER":"layover"}, {"LOWER": "at"}, {"POS":"PROPN", "OP":"+"},{"POS":{"IN":["PUNCT", "SYM", "CCONJ"]}, "OP":"?"}, 
        {"POS":"PROPN", "OP":"*"}, {"TEXT": "Field"}, {"LOWER": "in"}, {"POS": "PROPN", "OP":"*"}, {"POS":"PROPN", "OP":"+"}]
        ]
    connecting_airport_pattern_3 = [
        [{"LOWER":"layover"}, {"LOWER": "at"}, {"POS":"PROPN", "OP":"+"}, {"LOWER":"in"}, {"POS":"PROPN", "OP":"+"}],
        ]
    num_of_carryon_pattern = [
        [{"POS": "PUNCT"}, {"LOWER": "carry"}, {"POS":"PUNCT"}, {"LOWER":"on"}]
    ]
    num_of_carryon_pattern_2 = [
        [{"POS": "NUM"}, {"LOWER": "carry"}, {"POS":"PUNCT"}, {"LOWER":"on"}]
    ]
    num_of_checked_pattern = [
        [{"POS": "NUM"}, {"LOWER": "checked"}, {"LOWER": "bags"}]
    ]

    #test_pattern = [
    #    [{"LOWER":"layover"}, {"LOWER": "at"}, {"POS":"PROPN", "OP":"+"}, {"POS":{"IN":["PUNCT", "SYM", "CCONJ"]}, "OP":"?"}, {"POS":"PROPN","OP":"*"}, {"TEXT": "Airport"}, {"LOWER": "in"}, {"POS": "PROPN", "OP":"+"}]
    #]
    '''We're here for debugging'''
    matcher.add("FLIGHT_DURATION", duration_pattern) # correct
    latest = None
    matches = matcher(nlp_doc)
    
    span = nlp_doc[matches[-1][1]:matches[-1][2]]
    latest = span.text
    extracted.append(latest)
    
    matcher.remove("FLIGHT_DURATION")
    matcher.add("FLIGHT_PRICE", price_pattern) # correct
    matcher.add("NUM_STOPS", num_stops_pattern) # correct
    matcher.add("NO_STOPS", no_stops_pattern) # correct
    matcher.add("DEPARTURE_TIME", departure_time_pattern, greedy='LONGEST')
    matcher.add("ARRIVAL_TIME", arrival_time_pattern, greedy='LONGEST')
    #matcher.add("ARRIVAL_TIME_2", arrival_time_pattern_2, greedy='LONGEST')

    matcher.add("AIRLINE", airline_pattern, greedy='LONGEST') # correct
    matcher.add("NUM_CARRYON", num_of_carryon_pattern) # correct
    matcher.add("NUM_CARRYON_2", num_of_carryon_pattern_2) # correct
    matcher.add("NUM_CHECKED", num_of_checked_pattern) # correct
    matches = matcher(nlp_doc)
    for match_id, start, end in matches:
        span = nlp_doc[start:end]
        print(span.text)
        extracted.append(span.text)
    clear_matcher(matcher)
    #matcher.add("TEST_PATTERN", test_pattern, greedy='LONGEST')
    matcher.add("CONNECTING_AIRPORT", connecting_airport_pattern, greedy='LONGEST')
    #matcher.add("CONNECTING_AIRPORT_2", connecting_airport_pattern_2, greedy='LONGEST')
    #matcher.add("CONNECTING_AIRPORT_3", connecting_airport_pattern_3, greedy='LONGEST')
    matcher.add("LAYOVER_DURATION", layover_duration_pattern) # correct
    matcher.add("LAYOVER_DURATION_2", layover_duration_pattern_2) # correct
    matcher.add("LAYOVER_DURATION_3", layover_duration_pattern_3) # correct
    latest = None
    matches = matcher(nlp_doc)
    for match_id, start, end in matches:
        span = nlp_doc[start:end]
        print(span.text)
        extracted.append(span.text)
    clear_matcher(matcher)
    return clean_data(extracted) 
    # Get round trip or one way from user input

def clear_matcher(matcher):
    for pattern in list(matcher._patterns.keys()):
        matcher.remove(pattern)

def getUserOriginDest():
    '''Retrieve the Seating Class'''
    while True:
        try:
            origin = input("Where from? ")
            origin_match = re.search("[a-zA-Z]+, [a-zA-Z]+", origin)
            if len(origin) < 2 or origin_match is None:
                print("Please enter a location. ")
            else:
                break
        except:
            print("Please enter a location.")
    
    while True:
        try:
            dest = input("Where to?: ")
            dest_match = re.search("[a-zA-Z]+, [a-zA-Z]+", dest)
            if len(dest) < 2 or dest_match is None:
                print("Please enter a location. ")
            else:
                break
        except:
            print("Please enter a location.")
            
    return origin, dest 

def add_months(current_date, months_to_add):
    new_date = datetime(current_date.year + (current_date.month + months_to_add - 1) // 12,
                        (current_date.month + months_to_add - 1) % 12 + 1,
                        current_date.day, current_date.hour, current_date.minute, current_date.second)
    return new_date


def getUserDate():
    '''Definitely fix the date validation later on'''
    flexible_date = True
    while True:
        try:
            date_type = input("Would you want a flexible or specific way to enter your departure and arrival dates? ")
            if date_type.lower() in ["flexible", "specific"]:
                break
            else:
                print("Please enter valid type.")
        except:
            print("Please enter valid type.")
    
    if date_type.lower() == "flexible":
        flex_months = []
        for num in range(6):
            current_date = datetime.now()
            future_month = add_months(current_date, num)
            flex_months.append(str(future_month.strftime("%B")))
        
        while True:
            try:
                user_month = input(f"Which month? All {' '.join([month for month in flex_months])} ")
                if user_month in flex_months or user_month.lower() == "all":
                    break
                else:
                    print("Choose one of the options above.")
            except:
                print("Choose one of the options above.")
        while True:
            try:
                user_length = input(f"How Long? Weekend, 1 Week, 2 Weeks ")
                if user_length in ["Weekend", "1 Week", "2 Weeks"]:
                    break
                else:
                    print("Choose one of the options above.")
            except:
                print("Choose one of the options above.")
        return user_month, user_length, flexible_date
    else:
        flexible_date = False
        while True:
            try:
                departure_date = input("When's the date to depart? ")
                date_match = re.match(r"\d+(/)\d+(/)\d+", departure_date)
                if date_match is not None:
                    break
                else:
                    print("Enter a valid date.")  
            except:
                print("Enter a valid date.")  
                
        while True:
            try:
                arrival_date = input("When's the date to arrive? ")
                date_match = re.match(r"\d+(/)\d+(/)\d+", arrival_date)
                if date_match is not None:
                    break
                else:
                    print("Enter a valid date.")  
            except:
                print("Enter a valid date.")  
        add_months(datetime.now(), 6)
    
    return departure_date, arrival_date, flexible_date
            
def getUserNumPass():
    '''Retrieve the number of passengers'''
    passangers = 9
    while True:
        try:
            num_adults = int(input(f"Enter the number of Adults: "))
            if num_adults > passangers:
                print("The maximum number of passengers is 9")
            else:
                passangers = passangers - num_adults if passangers - num_adults >= 0 else 0
                try:
                    num_child = int(input(f"Enter the number of Children (Aged 2-11): "))
                    if num_child > passangers:
                        print("The maximum number of passengers is 9")
                    else:
                        passangers = passangers - num_child if passangers - num_child >= 0 else 0
                        try:
                            num_infants_in_seat = int(input(f"Enter the number of Infants (In seat): "))
                            if num_infants_in_seat > passangers:
                                print("The maximum number of passengers is 9")
                            else:
                                passangers = passangers - num_infants_in_seat if passangers - num_infants_in_seat >= 0 else 0
                                try:
                                    num_infants_on_lap = int(input(f"Enter the number of Adults: "))
                                    if num_infants_on_lap > passangers:
                                        print("The maximum number of passengers is 9")
                                    if num_infants_on_lap > num_adults:
                                        print("The number of infants on lap cannot exceed the number of adults")
                                    else:
                                        passangers = passangers - num_infants_on_lap if passangers - num_infants_on_lap >= 0 else 0
                                        break
                                except:
                                    print("Please enter a valid number")
                        except:
                            print("Please enter a valid number")
                except:
                    print("Please enter a valid number")
        except:
            print("Please enter a valid number")
            
    return num_adults, num_child, num_infants_in_seat, num_infants_on_lap

def getUserSeatingClass():
    '''Retrieve the Seating Class'''
    while True:
        try:
            seating_class = input("Enter the Seating Class (Economy, Prem Econ, Business, First Class): ")
            if seating_class.lower() in ["economy", "prem econ", "business", "first class"]:
                break
            else:
                print("Please enter a valid seating class")
        except:
            print("Please enter a valid seating class")
            
    return seating_class

def getUserRoundTrip():
    '''Retrieve the Round-Trip or One-Way'''
    round_trip = False
    while True:
        try:
            round_trip = input("Enter Round Trip or One Way: ")
            if round_trip.lower() == "round trip":
                round_trip = True
                break
            elif round_trip.lower() == "one way":
                round_trip = False
                break
            else:
                print("Please enter a valid option")
        except:
            print("Please enter a valid option")
            
    return round_trip

def accessroundTripInfo():
    all_results = driver.find_elements(By.XPATH, "//ul[@class='Rk10dc']/li")
    for result in all_results:
        select_flight = result.find_element(By.XPATH, ".//div[@class='gQ6yfe m7VU8c']")
        select_flight.click()
        driver.get(driver.current_url)
        view_more_flights = driver.find_element(By.XPATH, ".//div[@jsname='YdtKid']").find_element(By.XPATH, ".//button[@jsname='ornU0b']")
        view_more_flights.click()
        time.sleep(2)
        all_results = driver.find_elements(By.XPATH, "//ul[@class='Rk10dc']/li")
        randomHash = {}
        for result in all_results:
            try:
                aria_label = result.find_element(By.XPATH, ".//div[@class='JMc5Xc']").get_attribute("aria-label")
            except:
                print("")
            if aria_label is not None:
                print(aria_label + "\n")
            time.sleep(2)



def clean_data(data):
    '''Extracting/Cleaning the extracted data using regex'''
    cleaned_data = {}
    
    
    
    # Extract the number of stops
    if data[2] == "Nonstop":
        # Extract the flight price
        try:
            flight_price = re.search(r'\d+', data[1])
            cleaned_data["Price"] = flight_price.group()
            print(flight_price.group())
        except:
            cleaned_data["Price"] = "0"
            print("0")
        # Extract the number of stops
        cleaned_data["Number of Stops"] = "0"
        print("0")
        
        if len(data) > 5:
            # Extract the airline
            try:
                airline = re.search(r'\w+\Z', data[5])
                cleaned_data["Airline"] = airline.group()
                print(airline.group())
            except:
                cleaned_data["Airline"] = "Unknown"
                print("Unknown")
        else:
            # Extract the airline
            try:
                airline = re.search(r'\w+\Z', data[3])
                cleaned_data["Airline"] = airline.group()
                print(airline.group())
            except:
                cleaned_data["Airline"] = "Unknown"
                print("Unknown")

        
        # Extract the departure airport, time, and date
        try:
            departure_airport = re.search(r"Leaves (.+? Airport)", data[-2])
            cleaned_data["Departure Airport"] = departure_airport.group(1)
            print(departure_airport.group(1))
        except:
            cleaned_data["Departure Airport"] = "Unknown"
            print("Unknown")
        try:
            departure_time = re.search(r"(\d+:\d+ [AP]M)", data[-2])
            cleaned_data["Departure Time"] = departure_time.group(1)
            print(departure_time.group(1))
        except:
            cleaned_data["Departure Time"] = "Unknown"
            print("Unknown")
        try:
            departure_date = re.search(r"on (\w+, \w+ \d+)", data[-2])
            cleaned_data["Departure Date"] = departure_date.group(1)
            print(departure_date.group(1))
        except:
            cleaned_data["Departure Date"] = "Unknown"
            print("Unknown")
        

        # Extract the arrival airport, time, and date
        try:   
            arrival_airport = re.search(r"arrives at (.+? Airport)", data[-1])
            cleaned_data["Arrival Airport"] = arrival_airport.group(1)
            print(arrival_airport.group(1))
        except:
            cleaned_data["Arrival Airport"] = "Unknown"
            print("Unknown")
        try:
            arrival_time = re.search(r"(\d+:\d+ [AP]M)", data[-1])
            cleaned_data["Arrival Time"] = arrival_time.group(1)
            print(arrival_time.group(1))
        except:
            cleaned_data["Arrival Time"] = "Unknown"
            print("Unknown")
        try:
            arrival_date = re.search(r"on (\w+, \w+ \d+)", data[-1])
            cleaned_data["Arrival Date"] = arrival_date.group(1)
            print(arrival_date.group(1))
        except:
            cleaned_data["Arrival Date"] = "Unknown"
            print("Unknown")

        # Extract the number of carry-on bags
        try:
            num_carryon = re.search(r"\d+", data[3])
            cleaned_data["Number of Carry-On Bags"] = num_carryon.group()
            print(num_carryon.group())
        except:
            cleaned_data["Number of Carry-On Bags"] = "0"
            print("0")
            
        try:   # Extract the number of checked bags
            num_checked = re.search(r"\d+", data[4])
            cleaned_data["Number of Checked Bags"] = num_checked.group()
            print(num_checked.group())
            
        except:
            cleaned_data["Number of Checked Bags"] = "0"
            print("0")

    else:
        # data = [price, # stops, airline, departure info, arrival info, total duration, # layovers, layover duration, layover info, num carryon, num checked]
        try:
            flight_price = re.search(r'\d+', data[1])
            cleaned_data["Price"] = flight_price.group()
            print(flight_price.group())
        except:
            cleaned_data["Price"] = "0"
            print("0")
        try:
            num_stops = re.search(r'\d+', data[2])
            cleaned_data["Number of Stops"] = num_stops.group()
            print(num_stops.group())
        except:
            cleaned_data["Number of Stops"] = "0"
            print("0")
        num_stops = int(num_stops.group()) # Use this to split the if/else logic regarding the number of layovers

        # Extract the airline
        try:
            airline = re.search(r'\w+\Z', data[5]) # Has trouble with "American and Hawaiin" Format
            cleaned_data["Airline"] = airline.group()
            print(airline.group())
        except:
            cleaned_data["Airline"] =  "Unknown"
            print("Unknown")

        # Extract the departure airport, time, and date
        try:    
            departure_airport = re.search(r"Leaves (.+? Airport)", data[6])
            cleaned_data["Departure Airport"] = departure_airport.group(1)
            print(departure_airport.group(1))
        except:
            cleaned_data["Departure Airport"] = ("Unknown")
            print("Unknown")
        try:
            departure_time = re.search(r"(\d+:\d+ [AP]M)", data[6])
            cleaned_data["Departure Time"] = departure_time.group(1)
            print(departure_time.group(1))
        except:
            cleaned_data["Departure Time"] = "Unknown"
            print("Unknown")
        try:
            departure_date = re.search(r"on (\w+, \w+ \d+)", data[6])
            cleaned_data["Departure Date"] = departure_date.group(1)
            print(departure_date.group(1))
        except:
            cleaned_data["Departure Date"] = "Unknown"
            print("Unknown")


        # Extract the arrival airport, time, and date
        try:    
            arrival_airport = re.search(r"arrives at (.+? Airport)", data[7])
            cleaned_data["Arrival Airport"] = arrival_airport.group(1)
            print(arrival_airport.group(1))
        except:
            cleaned_data["Arrival Airport"] = "Unknown"
            print("Unknown")
        try:
            arrival_time = re.search(r"(\d+:\d+ [AP]M)", data[7])
            cleaned_data["Arrival Time"] = arrival_time.group(1)
            print(arrival_time.group(1))
        except:
            cleaned_data["Arrival Time"] = "Unknown"
            print("Unknown")
        try:
            arrival_date = re.search(r"on (\w+, \w+ \d+)", data[7])
            cleaned_data["Arrival Date"] = arrival_date.group(1)
            print(arrival_date.group(1))
        except:
            cleaned_data["Arrival Date"] = "Unknown"
            print("Unknown")
        try:
            # Extract the number of carry-on bags
            num_carryon = re.search(r"\d+", data[3])
            cleaned_data["Number of Carry-On Bags"] = num_carryon.group()
            print(num_carryon.group())
        except:
            cleaned_data["Number of Carry-On Bags"] = "0"
            print("0")

        # Extract the number of checked bags
        try:
            num_checked = re.search(r"\d+", data[4])
            cleaned_data["Number of Checked Bags"] = num_checked.group()
            print(num_checked.group())
        except: 
            cleaned_data["Number of Checked Bags"]  = "0"
            print("0")

        layover_info = {}
        if num_stops == 1:
            # Extract the layover duration
            layover_duration = re.search(r"(\d+ hr \d+ min)", data[-2]) # 6
            if layover_duration is None:
                layover_duration = re.search(r"(\d+ min)", data[-2])
                if layover_duration is None:
                    layover_duration = re.search(r"(\d+ hr)", data[-2])
            cleaned_data["Layover Duration"] = layover_duration.group(1)
            print(layover_duration.group(1))

            # Extract layover airport
            try:
                layover_airport = re.search(r"at (.+? Airport)", data[-1])
                if layover_airport is None:
                    layover_airport = re.search(r"at (.+? Field)", data[-1])
                cleaned_data["Layover Airport"] = layover_airport.group(1)
                print(layover_airport.group(1)) 
            except:
                cleaned_data["Layover Airport"] = "None"
                print(layover_airport.group(1))
            
            try:
                # Extract layover city
                layover_city = re.search(r"in (.+)", data[-1])
                cleaned_data["Layover City"] = layover_city.group(1)
                print(layover_city.group(1))
            except:
                cleaned_data["Layover City"] = "None"
                print("None")


        else:
            cnt = 1
            for i in range(8, 8+len(data[8:])-num_stops):
                # Create a list of layover info throw it into a dictionary as the value with the key being the layover number
                # Extract the layover duration
                layovers = {"Layover Duration": None, "Layover Airport": None, "Layover City": None}
                layover_duration = re.search(r"(\d+ hr \d+ min)", data[i]) # 6
                if layover_duration is None:
                    layover_duration = re.search(r"(\d+ min)", data[i])
                    if layover_duration is None:
                        layover_duration = re.search(r"(\d+ hr)", data[i])
                layovers["Layover Duration"] = layover_duration.group(1)
                print(layover_duration.group(1))

                # Extract layover airport
                layover_airport = re.search(r"at (.+? Airport)", data[i+num_stops])
                if layover_airport is None:
                    layover_airport = re.search(r"at (.+? Field)", data[i+num_stops])
                layovers["Layover Airport"] = layover_airport.group(1)
                print(layover_airport.group(1))

                # Extract layover city
                layover_city = re.search(r"in (.+)", data[i+num_stops])
                layovers["Layover City"] = layover_city.group(1)
                print(layover_city.group(1))
                layover_info[cnt] = layovers
                cnt += 1
            cleaned_data["Layovers"] = layover_info
                

    # Extract the total duration of the flight
    try:
        total_duration = re.search(r"(\d+ hr \d+ min)", data[0])
        if total_duration is None:
            total_duration = re.search(r"(\d+ min)", data[0])
            if total_duration is None:
                total_duration = re.search(r"(\d+ hr)", data[0])
        cleaned_data["Total Duration"] = total_duration.group(1)
        print(total_duration.group(1))
    except:
        cleaned_data["Total Duration"] = "0"

    
    return cleaned_data
    

    
def concate(cleaned_data, num_adults, num_children, num_infants_in_seat, num_infants_on_lap, seating_class, round_trip, airplane_type):
    cleaned_data.append(num_adults)
    cleaned_data.append(num_children)
    cleaned_data.append(num_infants_in_seat)
    cleaned_data.append(num_infants_on_lap)
    cleaned_data.append(seating_class)
    cleaned_data.append(round_trip)
    cleaned_data.append(airplane_type)
    return cleaned_data


def insert_roundtrip(cursor, total_price, num_passengers):
    '''Insert roundtrip information and return the roundtrip ID'''
    cursor.execute(
        "INSERT INTO roundtrips (total_price, num_passengers) VALUES (%s, %s) RETURNING roundtrip_id",
        (total_price, num_passengers)
    )
    return cursor.fetchone()[0]


def insert_flight_features(cursor, one_way_info, flight_direction, airline_id, departure_airport_id, arrival_airport_id,
                          departure_airplane_id, arrival_airplane_id, user_data, roundtrip_id=None):
    '''Insert flight features and return the flight ID'''
    query = """
        INSERT INTO flight_features (
            flight_price, flight_direction, num_stops, airline_id, search_date, departure_airport_id,
            departure_time, departure_date, arrival_airport_id, arrival_time, arrival_date, travel_duration,
            num_layovers, num_carryon, num_checked, num_adults, num_children, num_infants_in_seat, num_infants_on_lap, seating_class,
            round_trip, departure_airplane_type_id, arrival_airplane_type_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING flight_id
    """
    if int(one_way_info["Number of Stops"]) != 0:
        values = (one_way_info["Price"], flight_direction, one_way_info["Number of Stops"], airline_id, user_data[7], departure_airport_id,
            one_way_info["Departure Time"], one_way_info["Departure Date"], arrival_airport_id, one_way_info["Arrival Time"], one_way_info["Arrival Date"], one_way_info["Total Duration"],
            one_way_info["Number of Stops"], one_way_info["Number of Carry-On Bags"], one_way_info["Number of Checked Bags"], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[8],
            departure_airplane_id, arrival_airplane_id)
    else:
        
        values = (
            one_way_info["Price"], flight_direction, one_way_info["Number of Stops"], airline_id, user_data[7], departure_airport_id,
            one_way_info["Departure Time"], one_way_info["Departure Date"], arrival_airport_id, one_way_info["Arrival Time"], one_way_info["Arrival Date"], one_way_info["Total Duration"],
            one_way_info["Number of Stops"], one_way_info["Number of Carry-On Bags"], one_way_info["Number of Checked Bags"], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[8],
            departure_airplane_id, arrival_airplane_id
        )
    if roundtrip_id:
        query = query.replace("flight_direction", "roundtrip_id, flight_direction")
        values = (one_way_info[0], roundtrip_id, flight_direction, *values[2:])
    
    cursor.execute(query, values)
    return cursor.fetchone()[0]


def insert_layover(cursor, flight_id, layover_airport_id, layover_duration):
    '''Insert layover information'''
    cursor.execute(
        "INSERT INTO layovers (flight_id, layover_airport_id, layover_duration) VALUES (%s, %s, %s)",
        (flight_id, layover_airport_id, layover_duration)
    )

def get_or_insert_id(cursor, table, column, value, return_column, additional_columns=None):
    '''Get or insert a value into a table'''
    cursor.execute(f"SELECT {return_column} FROM {table} WHERE {column} = %s", (value,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        if additional_columns:
            cursor.execute(f"INSERT INTO {table} ({column}, {', '.join(additional_columns.keys())}) VALUES (%s, {', '.join(['%s' for _ in additional_columns.keys()])}) RETURNING {return_column}", (value, *additional_columns.values()))
        else:
            cursor.execute(f"INSERT INTO {table} ({column}) VALUES (%s) RETURNING {return_column}", (value,))
        return cursor.fetchone()[0]

def pipeline(cleaned_data, user_data):
    '''Pipeline to store data into SQL database'''
    #['348', '1', 'Frontier', 'Baltimore/Washington International Thurgood Marshall Airport', '6:44 PM', 'Sunday, January 5', 'Denver International Airport', '7:04 AM', 'Monday, January 6', '14 hr 20 min', '1', '8 hr 22 min', 'Hartsfield-Jackson Atlanta International Airport', 'Atlanta', '0', '0', 2, 1, 0, 0, 'Economy', True, 'Airbus A320neo']
    # Initialize PostgreSQL DB
    connection, cursor = intializeDatabase()
    
    flight_direction = "Outgoing"
    ttl_passengers = sum(user_data[2:6])
        
    for scraped_info in cleaned_data:
        # Change one_way_info to dictionary
        one_way_info = scraped_info["One-Way Info"]
        airline_id = get_or_insert_id(cursor, "airlines", "airline_name", one_way_info["Airline"], "airline_id")
        try:
            if scraped_info["Departure Airplane Type"]:
                departure_airplane_id = get_or_insert_id(cursor, "airplanes", "airplane_type", scraped_info["Departure Airplane Type"], "airplane_id")
                arrival_airplane_id = get_or_insert_id(cursor, "airplanes", "airplane_type", scraped_info["Arrival Airplane Type"], "airplane_id")
        except KeyError:
            continue
        departure_airport_id = get_or_insert_id(cursor, "airports", "airport_name", one_way_info["Departure Airport"], "airport_id", {"city": user_data[0]})
        arrival_airport_id = get_or_insert_id(cursor, "airports", "airport_name", one_way_info["Arrival Airport"], "airport_id", {"city": user_data[1]})
        
        roundtrip_id = None
        if user_data[-1]:
            flight_direction = "Returning"
            roundtrip_id = get_or_insert_id(cursor, "roundtrips", "total_price", cleaned_data[-1], "roundtrip_id", {"num_passengers": ttl_passengers})
            connection.commit()
        
        flight_id = insert_flight_features(cursor, one_way_info, flight_direction, airline_id, departure_airport_id, arrival_airport_id, departure_airplane_id, arrival_airplane_id, user_data, roundtrip_id)
        connection.commit()
        if len(one_way_info) > 12 and int(one_way_info["Number of Stops"]) != 0:  # If there are layovers
            if int(one_way_info["Number of Stops"]) == 1:
                layover_airport_id = get_or_insert_id(cursor, 'airports', 'airport_name', one_way_info["Layover Airport"], 'airport_id', {'city': one_way_info["Layover City"]})
                insert_layover(cursor, flight_id, layover_airport_id, one_way_info["Layover Duration"])
                connection.commit()
            else:
                for _, layover_info in one_way_info["Layovers"].items():
                    layover_airport_id = get_or_insert_id(cursor, 'airports', 'airport_name', layover_info["Layover Airport"], 'airport_id', {'city': layover_info["Layover City"]})
                    insert_layover(cursor, flight_id, layover_airport_id, layover_info["Layover Duration"])
                    connection.commit()

    print("\n\tFinished.")
    closeConnection(connection, cursor)

def createLog(element):
    '''Create a log file'''
    logging.basicConfig(
        filename= datetime.now().strftime("scrape.log"),
        level = logging.WARNING,
        format = "%(asctime)s:%(levelname)s:%(message)s",
        datefmt = "%m/%d/%Y %I:%M:%S %p",
    )
    logging.warning(f"Log file created at this point {element}")
    
    
def driver():
    #pipeline(['211', '2', 'Southwest', 'Baltimore/Washington International Thurgood Marshall Airport', '5:35 PM', 'Thursday, April 3', 'Albany International Airport', '11:30 PM', 'Thursday, April 3', '1', '2', {1: ['35 min', 'Cleveland Hopkins International Airport', 'Cleveland'], 2: ['45 min', 'Chicago Midway International Airport', 'Chicago']}, '5 hr 55 min'], ["", "", 0, 0, 0, 0, 1, True])
    #exit()
    '''
    string = "From 4037 US dollars. 4 stops flight with Delta, Virgin Atlantic and Airlink. Leaves Baltimore/Washington International Thurgood Marshall Airport at 12:00 PM on Thursday, March 20 and arrives at Saint Helena Airport at 1:15 PM on Saturday, March 22. Total duration 45 hr 15 min. Layover (1 of 4) is a 4 hr 16 min layover at Hartsfield-Jackson Atlanta International Airport in Atlanta. Layover (2 of 4) is a 12 hr layover at Heathrow Airport in London. Layover (3 of 4) is a 1 hr 5 min layover at Cape Town International Airport in Cape Town. Layover (4 of 4) is a 30 min layover at Walvis Bay International Airport in Walvis Bay. Carbon emissions estimate: 1,665 kilograms. Select flight" #"From 706 US dollars. 2 stops flight with Icelandair and Scandinavian Airlines. Operated by Sas Connect. Leaves Baltimore/Washington International Thurgood Marshall Airport at 8:30 PM on Sunday, March 30 and arrives at Athens International Airport "Eleftherios Venizelos" at 6:50 PM on Monday, March 31. Total duration 15 hr 20 min. Layover (1 of 2) is a 1 hr 15 min layover at Keflavík International Airport in Reykjavík. Layover (2 of 2) is a 1 hr 35 min layover at Copenhagen Airport in Copenhagen. Select flight"
    print(string)
    doc = nlp(string)
    for token in doc:
        print(f"Token: {token.text}, Lemma: {token.lemma_}, POS: {token.pos_}, Tag: {token.tag_}, Dep: {token.dep_}, Shape: {token.shape_}, is_alpha: {token.is_alpha}, is_stop: {token.is_stop}")
    extractFlightInfo(doc)
    exit()
    '''
    seating_class = ["Economy", "Prem Econ", "Business", "First Class"]
    f = open("/home/mahl/Senior-Capstone/scraper/Progress.txt", "r")
    cnt = int(f.read())
    cnt = cnt % 50
    print(cnt)
    state_caps = [
    "Montgomery, Alabama", "Phoenix, Arizona", "Little Rock, Arkansas", "Sacramento, California", 
    "Denver, Colorado", "Hartford, Connecticut", "Tallahassee, Florida", "Atlanta, Georgia", 
    "Honolulu, Hawaii", "Boise, Idaho", "Springfield, Illinois", "Indianapolis, Indiana", 
    "Des Moines, Iowa", "Topeka, Kansas", "Frankfort, Kentucky", "Baton Rouge, Louisiana", 
    "Augusta, Maine", "Boston, Massachusetts", "Lansing, Michigan", "Saint Paul, Minnesota", 
    "Jackson, Mississippi", "Jefferson City, Missouri", "Helena, Montana", "Carson City, Nevada", 
    "Concord, New Hampshire", "Santa Fe, New Mexico", "Albany, New York", "Raleigh, North Carolina", 
    "Bismarck, North Dakota", "Columbus, Ohio", "Oklahoma City, Oklahoma", "Salem, Oregon", 
    "Providence, Rhode Island", "Columbia, South Carolina", "Pierre, South Dakota", "Nashville, Tennessee", 
    "Austin, Texas", "Salt Lake City, Utah", "Montpelier, Vermont", "Richmond, Virginia", 
    "Olympia, Washington", "Charleston, West Virginia", "Madison, Wisconsin", "Cheyenne, Wyoming"
]
    print(len(state_caps))
    start = time.perf_counter()
    
    for capitals in state_caps[cnt:]:
        with open("/home/mahl/Senior-Capstone/scraper/Progress.txt", "w") as f:
            f.write(f"{cnt}")
        f.close()
        for s_class in seating_class:
            tic = time.perf_counter()
            cnt += 1
            current_date = datetime.now().date()
            URL = "https://www.google.com/travel/explore"
            driver, wait = intialize(URL)
            accessOriginDestination(wait, driver, "BWI ", f"{capitals} ")
            access_Flights(driver)
            changeRoundTrip(wait, driver, False)
            accessSeatingClass(wait, driver, s_class)
            extraced_flight_info = retrieveFlightDetails(driver, wait, False)
            
            user_data = ["BWI", f"{capitals}", 1, 0, 0, 0, s_class, current_date, False]
            createLog(capitals)
            pipeline(extraced_flight_info, user_data)
            print("\nComplete.")
            driver.close()
            toc = time.perf_counter()
            print(f"Time elapsed: {toc-tic}")
    
    stop = time.perf_counter()
    print(f"Overall Execution: {stop-start}")
    with open("Progress.txt", "w") as f:
            f.write("0")
    f.close()
    exit()
    '''Some User-centric Motion'''
    URL = "https://www.google.com/travel/explore"
    driver, wait = intialize(URL)
    
    origin, dest = getUserOriginDest()
    accessOriginDestination(wait, driver, origin, dest)
    round_trip = getUserRoundTrip()
    changeRoundTrip(wait, driver, round_trip)
    num_adults, num_children, num_infants_in_seat, num_infants_on_lap = getUserNumPass()
    accessNumOfPassengers(wait, driver, num_adults, num_children, num_infants_in_seat, num_infants_on_lap)
    date1, date2, flexible_date = getUserDate() # date1 = user_month, date2 = user_length, flexible_date = True| or | # date1 = departure_date, date2 = arrival_date # flexible_date = False
    if flexible_date:
        accessFlexibleDates(wait, driver, date1, date2)
    else:
        accessSpecificDates(wait, driver, date1, date2)
    current_date = datetime.now()
    seating_class = getUserSeatingClass()
    accessSeatingClass(wait, driver, seating_class)
    access_Flights(driver)
    extraced_flight_info = retrieveFlightDetails(driver, wait, round_trip)
    user_data = [origin, dest, num_adults, num_children, num_infants_in_seat, num_infants_on_lap, seating_class, current_date, round_trip]
    
    
    
    # retrieve search date
    exit()
    # Round-trip flight details
    URL = ""
    driver, wait = intialize(URL)
    origin = "Baltimore" # origin, dest = getUserLocations()
    dest = "Denver"
    num_adults, num_children, num_infants_in_seat, num_infants_on_lap = 2, 1, 0, 0 #getUserNumPass()
    accessNumOfPassengers(wait, driver, num_adults, num_children, num_infants_in_seat, num_infants_on_lap) # Access the number of passengers for user
    seating_class = "Economy" #getUserSeatingClass()
    accessSeatingClass(wait, driver, seating_class) # Access the seating class for user
    round_trip = False #getUserRoundTrip()
    changeRoundTrip(wait, driver, round_trip)
    airplane_type = retrieveAirplaneType(driver)
    data = ['348 US dollars', '1 stop flight', 'with Frontier', 'Leaves Baltimore/Washington International Thurgood Marshall Airport at 6:44 PM on Sunday, January 5', 'arrives at Denver International Airport at 7:04 AM on Monday, January 6', 'Total duration 14 hr 20 min', 'Layover (1 of 1)', 'is a 8 hr 22 min', 'layover at Hartsfield-Jackson Atlanta International Airport in Atlanta', '0 carry-on bags', '0 checked bags']
    cleaned = clean_data(data)
    cleaned = concate(cleaned, num_adults, num_children, num_infants_in_seat, num_infants_on_lap, seating_class, round_trip, airplane_type)
    print(cleaned)
    pipeline(cleaned, [origin, dest])
    exit()
    
    '''
    #Retrieve User Input
    accessSpecificDates(wait, driver, "1/5/2025", "1/10/2025") # Access Specific Dates for user
    accessFlexibleDates(wait, driver, "January", "2 weeks") # Access Flexible Dates for user
    accessOriginDestination(wait, driver, "BWI", "LAX") # Access the origin and destination for user

    
    
    
    
    exit()
    
    
    
    
    # NLP Stuff for data scrape
    # Google Flights Flights page
    #driver = webdriver.Chrome()
    #driver.get("https://www.google.com/travel/flights/search?tfs=CBwQAhojEgoyMDI1LTAxLTA1agcIARIDQldJcgwIAhIIL20vMDJjbDEaIxIKMjAyNS0wMS0wNmoMCAISCC9tLzAyY2wxcgcIARIDQldJQAFIAXABggELCP___________wGYAQE&tfu=EgYIABABGAA&tcfs=ChUKCC9tLzA5NGp2GglCYWx0aW1vcmVSBGABeAE")
    #Retrieve Departing flights
    best_results = driver.find_elements(By.XPATH, "//ul[@class='Rk10dc']/li")
    randomHash = {}
    
    for result in best_results:
        aria_label = result.find_element(By.XPATH, ".//div[@class='JMc5Xc']").get_attribute("aria-label")
        if aria_label is not None:
            print(aria_label + "\n")
            doc = nlp(aria_label)
            extractFlightInfo(doc)
            exit()
            # Comment Out below
            # Basic Text Token Analysis
            for token in doc:
                vals = list((token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop))
                randomHash[token.text] = vals
                #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,token.shape_, token.is_alpha, token.is_stop)
            print(randomHash)
            
            exit()
            
    time.sleep(5)
    
    exit()
    '''

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)
driver()

# aria-label='Some text' is your best bet for finding elements
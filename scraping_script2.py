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
    file = open("./psql_credentials.txt", "r")
    creds = file.readlines()
    creds = [cred.strip("\n") for cred in creds]
    file.close()
    '''Initialize the database'''
    conn = psycopg2.connect(
        host=f"{creds[0]}",
        database=f"{creds[1]}",
        user=f"{creds[2]}",
        password=f"{creds[3]}",
        port = f"{creds[4]}"
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
    if class_type == "Economy".lower():
        class_type_button = driver.find_element(By.CSS_SELECTOR, "ul[aria-label='Select your preferred seating class.']").find_element(By.CSS_SELECTOR, "li[data-value='1']") # 1 = Economy, 2 = Prem Econ, 3 = Business, 4 = First
        class_type_button.click()
    if class_type == "Prem Econ".lower():
        class_type_button = driver.find_element(By.CSS_SELECTOR, "ul[aria-label='Select your preferred seating class.']").find_element(By.CSS_SELECTOR, "li[data-value='2']") # 1 = Economy, 2 = Prem Econ, 3 = Business, 4 = First
        class_type_button.click()
    if class_type == "Business".lower():
        class_type_button = driver.find_element(By.CSS_SELECTOR, "ul[aria-label='Select your preferred seating class.']").find_element(By.CSS_SELECTOR, "li[data-value='3']") # 1 = Economy, 2 = Prem Econ, 3 = Business, 4 = First
        class_type_button.click()
    if class_type == "First Class".lower():
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
            dropdown_button = result.find_element(By.CSS_SELECTOR, "div[jsname='UsVyAb']").find_element(By.CSS_SELECTOR, "button[jsname='LgbsSe']")#.find_element(By.XPATH, "//Button[jsname='LgbsSe']")
            dropdown_button.click()
            driver.execute_script("arguments[0].scrollIntoView(true);", dropdown_button)
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
         [{"TEXT": "Total"}, {"TEXT": "duration"}, {"POS": "NUM"}, {"LOWER": "hr"}, {"POS": "NUM", "OP":"?"}, {"LOWER": "min", "OP":"?"}]
    ]
    '''May need to change later'''
    num_layover_pattern = [
        [{"TEXT": "Layover"}, {"TEXT": "("}, {"POS": "NUM"}, {"TEXT": "of"}, {"POS": "NUM"}, {"TEXT": ")"}]
    ]
    
    layover_duration_pattern = [
        [{"POS": "NUM"}, {"LOWER": "hr"}, {"POS": "NUM"}, {"LOWER": "min"}, {"LOWER": "layover"}], 
        [{"POS": "NUM"}, {"LOWER": "min"}, {"LOWER", "layover"}]
    ]
    
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
        {"POS": {"IN": ["SYM", "PUNCT", "CCONJ"]}, "OP": "?"}, {"POS": "PROPN", "OP": "+"}, {"TEXT": "Airport"}, {"LOWER":"at"}, {"POS": "NUM"}, {"IS_SPACE": True, "OP": "*"}, 
        {"LOWER": {"IN": ["am", "pm"]}}, {"LOWER": "on"}, {"POS": "PROPN"}, {"TEXT": ","}, {"POS":"PROPN"}, {"POS": "NUM"}]
       ]
    
    layover_duration_pattern = [
        [{"LOWER":"is"}, {"LOWER":"a"}, {"POS": "NUM"}, {"LOWER": "hr"}, {"POS": "NUM", "OP":"+"}, {"LOWER": "min", "OP":"+"}]
    ]
    
    layover_duration_pattern_2 = [
        [{"LOWER":"is"}, {"LOWER":"a"}, {"POS": "NUM"}, {"LOWER": "min"}]
    ]
    
    layover_duration_pattern_3 = [
        [{"LOWER":"is"}, {"LOWER":"a"}, {"POS": "NUM"}, {"LOWER": "hr"}, {"LOWER":"layover"}]
    ]
    
    airline_pattern = [
        [{"LOWER": "with"}, {"POS": "PROPN"}]
    ]
    connecting_airport_pattern = [
        [{"LOWER":"layover"}, {"LOWER": "at"}, {"POS":"PROPN", "OP":"+"},{"POS":{"IN":["PUNCT", "SYM", "CCONJ"]}, "OP":"?"}, 
         {"POS":"PROPN", "OP":"+"}, {"TEXT": "Airport"}, {"LOWER": "in"}, {"POS": "PROPN"}, {"POS":"PROPN", "OP":"?"}]
        ]
    connecting_airport_pattern_2 = [
        [{"LOWER":"layover"}, {"LOWER": "at"}, {"POS":"PROPN", "OP":"+"},{"POS":{"IN":["PUNCT", "SYM", "CCONJ"]}, "OP":"?"}, 
        {"POS":"PROPN", "OP":"+"}, {"TEXT": "Field"}, {"LOWER": "in"}, {"POS": "PROPN", "OP":"*"}, {"POS":"PROPN", "OP":"?"}]
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
    '''We're here for debugging'''
    matcher.add("FLIGHT_DURATION", duration_pattern) # correct
    latest = None
    matches = matcher(nlp_doc)
    
    span = nlp_doc[matches[-1][1]:matches[-1][2]]
    latest = span.text
    
    extracted.append(latest)
    matcher.remove("FLIGHT_DURATION")
    matcher.add("CONNECTING_AIRPORT", connecting_airport_pattern)
    matcher.add("CONNECTING_AIRPORT_2", connecting_airport_pattern_2)
    latest = None
    matches = matcher(nlp_doc)
    if matches:
        span = nlp_doc[matches[-1][1]:matches[-1][2]]
        latest = span.text
    
        extracted.append(latest)
    
    matcher.remove("CONNECTING_AIRPORT")
    matcher.remove("CONNECTING_AIRPORT_2")
    matcher.add("FLIGHT_PRICE", price_pattern) # correct
    matcher.add("NUM_STOPS", num_stops_pattern) # correct
    matcher.add("NO_STOPS", no_stops_pattern) # correct
    matcher.add("NUM_LAYOVERS", num_layover_pattern) # correct
    matcher.add("LAYOVER_DURATION", layover_duration_pattern) # correct
    matcher.add("LAYOVER_DURATION_2", layover_duration_pattern_2) # correct
    matcher.add("LAYOVER_DURATION_3", layover_duration_pattern_3) # correct
    matcher.add("DEPARTURE_TIME", departure_time_pattern)
    matcher.add("ARRIVAL_TIME", arrival_time_pattern)

    matcher.add("AIRLINE", airline_pattern) # correct
    matcher.add("NUM_CARRYON", num_of_carryon_pattern) # correct
    matcher.add("NUM_CARRYON_2", num_of_carryon_pattern_2) # correct
    matcher.add("NUM_CHECKED", num_of_checked_pattern) # correct
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
    cleaned_data = []
    
    
    
    # Extract the number of stops
    if data[2] == "Nonstop":
        # Extract the flight price
        flight_price = re.search(r'\d+', data[1])
        cleaned_data.append(flight_price.group())
        print(flight_price.group())
        cleaned_data.append("0")
        print(data[1])
        # Extract the number of carry-on bags
        if len(data) > 6:
            num_carryon = re.search(r"\d+", data[6])
            cleaned_data.append(num_carryon.group())
            print(num_carryon.group())
            
            # Extract the number of checked bags
            num_checked = re.search(r"\d+", data[7])
            cleaned_data.append(num_checked.group())
            print(num_checked.group())
        # Extract the airline
        airline = re.search(r'\w+\Z', data[3])
        cleaned_data.append(airline.group())
        print(airline.group())
        # Extract the departure airport, time, and date
        departure_airport = re.search(r"Leaves (.+? Airport)", data[4])
        cleaned_data.append(departure_airport.group(1))
        print(departure_airport.group(1))
        departure_time = re.search(r"(\d+:\d+ [AP]M)", data[4])
        cleaned_data.append(departure_time.group(1))
        print(departure_time.group(1))
        departure_date = re.search(r"on (\w+, \w+ \d+)", data[4])
        cleaned_data.append(departure_date.group(1))
        print(departure_date.group(1))
        

        # Extract the arrival airport, time, and date
        arrival_airport = re.search(r"arrives at (.+? Airport)", data[5])
        cleaned_data.append(arrival_airport.group(1))
        print(arrival_airport.group(1))
        arrival_time = re.search(r"(\d+:\d+ [AP]M)", data[5])
        cleaned_data.append(arrival_time.group(1))
        print(arrival_time.group(1))
        arrival_date = re.search(r"on (\w+, \w+ \d+)", data[5])
        cleaned_data.append(arrival_date.group(1))
        print(arrival_date.group(1))
            
    else:
        flight_price = re.search(r'\d+', data[2])
        cleaned_data.append(flight_price.group())
        print(flight_price.group())
        # data = [price, # stops, airline, departure info, arrival info, total duration, # layovers, layover duration, layover info, num carryon, num checked]
        num_stops = re.search(r'\d+', data[3])
        cleaned_data.append(num_stops.group())
        print(num_stops.group())
        num_stops = int(num_stops.group()) # Use this to split the if/else logic regarding the number of layovers
        '''May Need to change later'''
        # Extract the number of layovers
        #num_layovers = re.search(r"\d+", data[6]) # 5
        #cleaned_data.append(num_layovers.group())
        #print(num_layovers.group())
        # Extract the airline
        airline = re.search(r'\w+\Z', data[4])
        cleaned_data.append(airline.group())
        print(airline.group())
        
        # Extract the departure airport, time, and date
        departure_airport = re.search(r"Leaves (.+? Airport)", data[5])
        cleaned_data.append(departure_airport.group(1))
        print(departure_airport.group(1))
        departure_time = re.search(r"(\d+:\d+ [AP]M)", data[5])
        cleaned_data.append(departure_time.group(1))
        print(departure_time.group(1))
        departure_date = re.search(r"on (\w+, \w+ \d+)", data[5])
        cleaned_data.append(departure_date.group(1))
        print(departure_date.group(1))
        

        # Extract the arrival airport, time, and date
        arrival_airport = re.search(r"arrives at (.+? Airport)", data[6])
        cleaned_data.append(arrival_airport.group(1))
        print(arrival_airport.group(1))
        arrival_time = re.search(r"(\d+:\d+ [AP]M)", data[6])
        cleaned_data.append(arrival_time.group(1))
        print(arrival_time.group(1))
        arrival_date = re.search(r"on (\w+, \w+ \d+)", data[6])
        cleaned_data.append(arrival_date.group(1))
        print(arrival_date.group(1))
        
        if num_stops == 1:
            # Extract the layover duration
            layover_duration = re.search(r"(\d+ hr \d+ min)", data[8]) # 6
            if layover_duration is None:
                layover_duration = re.search(r"(\d+ min)", data[8])
                if layover_duration is None:
                    layover_duration = re.search(r"(\d+ hr)", data[8])
            cleaned_data.append(layover_duration.group(1))
            print(layover_duration.group(1))

            # Extract layover airport
            layover_airport = re.search(r"at (.+? Airport)", data[1])
            if layover_airport is None:
                layover_airport = re.search(r"at (.+? Field)", data[1])
            cleaned_data.append(layover_airport.group(1))
            print(layover_airport.group(1))

            # Extract layover city
            layover_city = re.search(r"in (.+)", data[1])
            cleaned_data.append(layover_city.group(1))
            print(layover_city.group(1))
            
            # Extract the number of carry-on bags
            num_carryon = re.search(r"\d+", data[-2])
            cleaned_data.append(num_carryon.group())
            print(num_carryon.group())
            
            # Extract the number of checked bags
            num_checked = re.search(r"\d+", data[-1])
            cleaned_data.append(num_checked.group())
            print(num_checked.group())
            
        else:
            layover_info = data[7:-2]
            for info in layover_info:
                pass
    
    # Extract the total duration of the flight
    total_duration = re.search(r"(\d+ hr \d+ min)", data[0])
    if total_duration is None:
        total_duration = re.search(r"(\d+ min)", data[0])
        if total_duration is None:
            total_duration = re.search(r"(\d+ hr)", data[0])
    cleaned_data.append(total_duration.group(1))
    print(total_duration.group(1))
    
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

def pipeline(cleaned_data, user_data):
    '''Pipeline to store data into SQL database'''
    #['348', '1', 'Frontier', 'Baltimore/Washington International Thurgood Marshall Airport', '6:44 PM', 'Sunday, January 5', 'Denver International Airport', '7:04 AM', 'Monday, January 6', '14 hr 20 min', '1', '8 hr 22 min', 'Hartsfield-Jackson Atlanta International Airport', 'Atlanta', '0', '0', 2, 1, 0, 0, 'Economy', True, 'Airbus A320neo']
    # Initialize PostgreSQL DB
    connection, cursor = intializeDatabase()
    
    flight_direction = "Outgoing"
    ttl_passengers = 0
    for num in user_data[2:5]:
        ttl_passengers += num
        
    for scraped_info in cleaned_data:
        one_way_info = scraped_info["One-Way Info"]
        
        if len(one_way_info) == 10:
                '''Airline'''
                print(f"Inserting airline \"{one_way_info[2]}\" into database...")
                cursor.execute("SELECT airline_id FROM airlines WHERE airline_name = %s", (one_way_info[2],))
                result = cursor.fetchone()
                
                if result:
                    airline_id = result[0]
                else:
                    cursor.execute(
                        "INSERT INTO airlines (airline_name) VALUES (%s) RETURNING airline_id", 
                        (one_way_info[2],))
                    connection.commit()
                    airline_id = cursor.fetchone()[0]
                
                '''Departure\Arrival Airplane'''
                departure_airplane = scraped_info["Departure Airplane Type"]
                print(f"Inserting departure airplane \"{departure_airplane}\" into database...")
                cursor.execute("SELECT airplane_id FROM airplanes WHERE airplane_type = %s", (departure_airplane,))
                result = cursor.fetchone()
                
                if result:
                    departure_airplane_id = result[0]
                else:
                    cursor.execute("INSERT INTO airplanes (airplane_type) VALUES (%s) RETURNING airplane_id",
                                (departure_airplane, ))
                    connection.commit()
                    departure_airplane_id = cursor.fetchone()[0]
                    
                '''Arrival Airplane Type'''
                arrival_airplane = scraped_info["Arrival Airplane Type"]
                print(f"Inserting arrival airplane \"{arrival_airplane}\" into database...")
                cursor.execute("SELECT airplane_id FROM airplanes WHERE airplane_type = %s", (arrival_airplane,))
                result = cursor.fetchone()
                
                if result:
                    arrival_airplane_id = result[0]
                else:
                    cursor.execute("INSERT INTO airplanes (airplane_type) VALUES (%s) RETURNING airplane_id",
                                (arrival_airplane, ))
                    connection.commit()
                    arrival_airplane_id = cursor.fetchone()[0]
                
                '''Departure\Arrival Airport'''
                print(f"Inserting Departure Airport: \"{one_way_info[3]}\" and \"{user_data[0]}\" into database...")
                cursor.execute("SELECT airport_id FROM airports WHERE airport_name = %s and city = %s", (one_way_info[3],user_data[0], ))
                result = cursor.fetchone()
                
                if result:
                    departure_airport_id = result[0]
                else:
                    cursor.execute("INSERT INTO airports (airport_name, city) VALUES (%s, %s) RETURNING airport_id",
                                (one_way_info[3], user_data[0], ))
                
                
                print(f"Inserting Arrival Airport: \"{one_way_info[6]}\" and \"{user_data[1]}\" into database...")
                cursor.execute("SELECT airport_id FROM airports WHERE airport_name = %s and city = %s", (one_way_info[6], user_data[1], ))
                result = cursor.fetchone()
                if result:
                    arrival_airport_id = result[0]
                else:
                    cursor.execute("INSERT INTO airports (airport_name, city) VALUES (%s, %s) RETURNING airport_id",
                                    (one_way_info[6], user_data[1], ))   
                
                roundtrip_id = None
                if user_data[-1] == True: # if roundtrip
                    flight_direction = "Returning"
                    rnd_trip_passengers = 0
                    print(f"Inserting \"{cleaned_data[-1]}\" and \"{ttl_passengers}\" into database...")
                    cursor.execute("INSERT INTO roundtrips (total_price, num_passengers) VALUES (%s, %s) RETURNING roundtrip_id",
                            (cleaned_data[-1], ttl_passengers, ) )
                    connection.commit()
                    roundtrip_id = cursor.fetchone()[0]
                    
                print(f"Inserting flight features into database...")
                if roundtrip_id:
                    cursor.execute(
                        "INSERT INTO flight_features (flight_price, roundtrip_id, flight_direction, num_stops, airline_id, search_date, departure_airport_id, departure_time, departure_date, arrival_airport_id, arrival_time, arrival_date, travel_duration, num_layovers, num_adults, num_children, num_infants_in_seat, num_infants_on_lap, seating_class, round_trip, departure_airplane_type_id, arrival_airplane_type_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING flight_id",
                            (one_way_info[0],  roundtrip_id, flight_direction, one_way_info[1], airline_id, user_data[7], departure_airport_id, one_way_info[4],  one_way_info[5], arrival_airport_id, one_way_info[7], one_way_info[8], one_way_info[9], one_way_info[1], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[8], departure_airplane_id, arrival_airplane_id,)
                            )  
                    connection.commit()
                else:
                    cursor.execute(
                        "INSERT INTO flight_features (flight_price, flight_direction, num_stops, airline_id, search_date, departure_airport_id, departure_time, departure_date, arrival_airport_id, arrival_time, arrival_date, travel_duration, num_layovers, num_adults, num_children, num_infants_in_seat, num_infants_on_lap, seating_class, round_trip, departure_airplane_type_id, arrival_airplane_type_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING flight_id",
                            (one_way_info[0], flight_direction, one_way_info[1], airline_id, user_data[7], departure_airport_id, one_way_info[4],  one_way_info[5], arrival_airport_id, one_way_info[7], one_way_info[8], one_way_info[9], one_way_info[1], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[8], departure_airplane_id, arrival_airplane_id,)
                            )
        elif len(one_way_info)>=12:  
            if one_way_info[1] == 0: # No stops
                '''Airline'''
                print(f"Inserting airline \"{one_way_info[4]}\" into database...")
                cursor.execute("SELECT airline_id FROM airlines WHERE airline_name = %s", (one_way_info[4],))
                result = cursor.fetchone()
                
                if result:
                    airline_id = result[0]
                else:
                    cursor.execute(
                        "INSERT INTO airlines (airline_name) VALUES (%s) RETURNING airline_id", 
                        (one_way_info[4],))
                    connection.commit()
                    airline_id = cursor.fetchone()[0]
                
                
                '''Departure\Arrival Airplane'''
                departure_airplane = scraped_info["Departure Airplane Type"]
                print(f"Inserting departure airplane \"{departure_airplane}\" into database...")
                cursor.execute("SELECT airplane_id FROM airplanes WHERE airplane_type = %s", (departure_airplane,))
                result = cursor.fetchone()
                
                if result:
                    departure_airplane_id = result[0]
                else:
                    cursor.execute("INSERT INTO airplanes (airplane_type) VALUES (%s) RETURNING airplane_id",
                                (departure_airplane, ))
                    connection.commit()
                    departure_airplane_id = cursor.fetchone()[0]
                ''''''
                arrival_airplane = scraped_info["Arrival Airplane Type"]
                print(f"Inserting arrival airplane \"{arrival_airplane}\" into database...")
                cursor.execute("SELECT airplane_id FROM airplanes WHERE airplane_type = %s", (arrival_airplane,))
                result = cursor.fetchone()
                
                if result:
                    arrival_airplane_id = result[0]
                else:
                    cursor.execute("INSERT INTO airplanes (airplane_type) VALUES (%s) RETURNING airplane_id",
                                (departure_airplane, ))
                    connection.commit()
                    arrival_airplane_id = cursor.fetchone()[0]
                
                '''Departure\Arrival Airport'''
                print(f"Inserting Departure Airport: \"{one_way_info[5]}\" and \"{user_data[0]}\" into database...")
                cursor.execute("SELECT airport_id FROM airports WHERE airport_name = %s and city = %s", (one_way_info[5],user_data[0], ))
                result = cursor.fetchone()
                
                if result:
                    departure_airport_id = result[0]
                else:
                    cursor.execute("INSERT INTO airports (airport_name, city) VALUES (%s, %s) RETURNING airport_id",
                                (one_way_info[5], user_data[0], )) # Origin airport as well as city
                    connection.commit()
                    departure_airport_id = cursor.fetchone()[0]
                
                print(f"Inserting Arrival Airport: \"{one_way_info[8]}\" and \"{user_data[1]}\" into database...")
                cursor.execute("SELEct airport_id FROM airports WHERE airport_name = %s and city = %s", (one_way_info[8], user_data[1], ))
                result = cursor.fetchone()
                
                if result:
                    arrival_airport_id = result[0]
                else:
                    cursor.execute("INSERT INTO airports (airport_name, city) VALUES (%s, %s) RETURNING airport_id",
                                    (one_way_info[8], user_data[1], )) # destination airport as well as city
                    connection.commit()
                    arrival_airport_id = cursor.fetchone()[0]
                
                roundtrip_id = None
                if user_data[-1] == True: # if roundtrip
                    flight_direction = "Returning"
                    rnd_trip_passengers = 0
                    print(f"Inserting \"{cleaned_data[-1]}\" and \"{ttl_passengers}\" into database...")
                    cursor.execute("INSERT INTO roundtrips (total_price, num_passengers) VALUES (%s, %s) RETURNING roundtrip_id",
                            (cleaned_data[-1], ttl_passengers, ) )
                    connection.commit()
                    roundtrip_id = cursor.fetchone()[0]
                    '''Work in Progress'''
                    # Some code here for round trip automation
                    #
                    #
                
                
                print(f"Inserting flight features into database...")
                if roundtrip_id:
                    cursor.execute(
                        "INSERT INTO flight_features (flight_price, roundtrip_id, flight_direction, num_stops, airline_id, search_date, departure_airport_id, departure_time, departure_date, arrival_airport_id, arrival_time, arrival_date, travel_duration, num_layovers, num_carryon, num_checked, num_adults, num_children, num_infants_in_seat, num_infants_on_lap, seating_class, round_trip, departure_airplane_type_id, arrival_airplane_type_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING flight_id",
                            (one_way_info[0],  roundtrip_id, flight_direction, one_way_info[1], airline_id, user_data[7], departure_airport_id, one_way_info[6],  one_way_info[7], arrival_airport_id, one_way_info[9], one_way_info[10], one_way_info[-1], one_way_info[1], one_way_info[2], one_way_info[3], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[8], departure_airplane_id, arrival_airplane_id,)
                            )  
                    connection.commit()
                else:
                    cursor.execute(
                        "INSERT INTO flight_features (flight_price, flight_direction, num_stops, airline_id, search_date, departure_airport_id, departure_time, departure_date, arrival_airport_id, arrival_time, arrival_date, travel_duration, num_layovers, num_carryon, num_checked, num_adults, num_children, num_infants_in_seat, num_infants_on_lap, seating_class, round_trip, departure_airplane_type_id, arrival_airplane_type_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING flight_id",
                            (one_way_info[0], flight_direction, one_way_info[1], airline_id, user_data[7], departure_airport_id, one_way_info[6],  one_way_info[7], arrival_airport_id, one_way_info[9], one_way_info[10], one_way_info[-1], one_way_info[1], one_way_info[2], one_way_info[3], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[8], departure_airplane_id, arrival_airplane_id,)
                            )  
                    connection.commit()
                flight_id = cursor.fetchone()[0]
                
                
                
            else: 
                
                '''Airline'''
                print(f"Inserting airline \"{one_way_info[2]}\" into database...")
                cursor.execute("SELECT airline_id FROM airlines WHERE airline_name = %s", (one_way_info[2],))
                result = cursor.fetchone()
                
                if result:
                    airline_id = result[0]
                else:
                    cursor.execute(
                        "INSERT INTO airlines (airline_name) VALUES (%s) RETURNING airline_id", 
                        (one_way_info[2],))
                    connection.commit()
                    airline_id = cursor.fetchone()[0]
                
                
                '''Departure\Arrival Airplane'''
                departure_airplane = scraped_info["Departure Airplane Type"]
                print(f"Inserting departure airplane \"{departure_airplane}\" into database...")
                cursor.execute("SELECT airplane_id FROM airplanes WHERE airplane_type = %s", (departure_airplane,))
                result = cursor.fetchone()
                
                if result:
                    departure_airplane_id = result[0]
                else:
                    cursor.execute("INSERT INTO airplanes (airplane_type) VALUES (%s) RETURNING airplane_id",
                                (departure_airplane, ))
                    connection.commit()
                    departure_airplane_id = cursor.fetchone()[0]
                ''''''
                arrival_airplane = scraped_info["Arrival Airplane Type"]
                print(f"Inserting arrival airplane \"{arrival_airplane}\" into database...")
                cursor.execute("SELECT airplane_id FROM airplanes WHERE airplane_type = %s", (arrival_airplane,))
                result = cursor.fetchone()
                
                if result:
                    arrival_airplane_id = result[0]
                else:
                    cursor.execute("INSERT INTO airplanes (airplane_type) VALUES (%s) RETURNING airplane_id",
                                (departure_airplane, ))
                    connection.commit()
                    arrival_airplane_id = cursor.fetchone()[0]
                
                '''Departure\Arrival Airport'''
                print(f"Inserting Departure Airport: \"{one_way_info[3]}\" and \"{user_data[0]}\" into database...")
                cursor.execute("SELECT airport_id FROM airports WHERE airport_name = %s and city = %s", (one_way_info[3],user_data[0], ))
                result = cursor.fetchone()
                
                if result:
                    departure_airport_id = result[0]
                else:
                    cursor.execute("INSERT INTO airports (airport_name, city) VALUES (%s, %s) RETURNING airport_id",
                                (one_way_info[3], user_data[0], )) # Origin airport as well as city
                    connection.commit()
                    departure_airport_id = cursor.fetchone()[0]
                
                print(f"Inserting Arrival Airport: \"{one_way_info[6]}\" and \"{user_data[1]}\" into database...")
                cursor.execute("SELEct airport_id FROM airports WHERE airport_name = %s and city = %s", (one_way_info[6], user_data[1], ))
                result = cursor.fetchone()
                
                if result:
                    arrival_airport_id = result[0]
                else:
                    cursor.execute("INSERT INTO airports (airport_name, city) VALUES (%s, %s) RETURNING airport_id",
                                    (one_way_info[6], user_data[1], )) # destination airport as well as city
                    connection.commit()
                    arrival_airport_id = cursor.fetchone()[0]
                
                roundtrip_id = None
                if user_data[-1] == True: # if roundtrip
                    flight_direction = "Returning"
                    rnd_trip_passengers = 0
                    print(f"Inserting \"{cleaned_data[-1]}\" and \"{ttl_passengers}\" into database...")
                    cursor.execute("INSERT INTO roundtrips (total_price, num_passengers) VALUES (%s, %s) RETURNING roundtrip_id",
                            (cleaned_data[-1], ttl_passengers, ) )
                    connection.commit()
                    roundtrip_id = cursor.fetchone()[0]
                
                
                print(f"Inserting flight features into database...")
                if roundtrip_id:
                    cursor.execute(
                        "INSERT INTO flight_features (flight_price, roundtrip_id, flight_direction, num_stops, airline_id, search_date, departure_airport_id, departure_time, departure_date, arrival_airport_id, arrival_time, arrival_date, travel_duration, num_layovers, num_carryon, num_checked, num_adults, num_children, num_infants_in_seat, num_infants_on_lap, seating_class, round_trip, departure_airplane_type_id, arrival_airplane_type_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING flight_id",
                            (one_way_info[0],  roundtrip_id, flight_direction, one_way_info[1], airline_id, user_data[7], departure_airport_id, one_way_info[4],  one_way_info[5], arrival_airport_id, one_way_info[7], one_way_info[8], one_way_info[-1], one_way_info[1], one_way_info[-3], one_way_info[-2], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[8], departure_airplane_id, arrival_airplane_id,)
                            )  
                    connection.commit()
                else:
                    cursor.execute(
                        "INSERT INTO flight_features (flight_price, flight_direction, num_stops, airline_id, search_date, departure_airport_id, departure_time, departure_date, arrival_airport_id, arrival_time, arrival_date, travel_duration, num_layovers, num_carryon, num_checked, num_adults, num_children, num_infants_in_seat, num_infants_on_lap, seating_class, round_trip, departure_airplane_type_id, arrival_airplane_type_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING flight_id",
                            (one_way_info[0], flight_direction, one_way_info[1], airline_id, user_data[7], departure_airport_id, one_way_info[4],  one_way_info[5], arrival_airport_id, one_way_info[7], one_way_info[8], one_way_info[-1], one_way_info[1], one_way_info[-3], one_way_info[-2], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[8], departure_airplane_id, arrival_airplane_id,)
                            )  
                    connection.commit()
                flight_id = cursor.fetchone()[0]
                
                '''Layover Airport'''
                print(f"Inserting \"{one_way_info[3]}\" into database...\n")
                cursor.execute("SELECT airport_id FROM airports WHERE airport_name = %s AND city = %s", (one_way_info[3], one_way_info[4],))
                result = cursor.fetchone()
                
                if result:
                    layover_airport_id = result[0]
                else:
                    cursor.execute("INSERT INTO airports (airport_name, city) VALUES (%s, %s) RETURNING airport_id",
                                (one_way_info[3], one_way_info[4], ) )
                    connection.commit()
                    layover_airport_id = cursor.fetchone()[0]
            
                cursor.execute(
                    "INSERT INTO layovers (flight_id, layover_airport_id, layover_duration) VALUES (%s, %s, %s)",
                    (flight_id, layover_airport_id, one_way_info[9], ) 
                    )
                connection.commit()
            
        else:   
            '''Airline'''
            print(f"Inserting airline \"{one_way_info[4]}\" into database...")
            cursor.execute("SELECT airline_id FROM airlines WHERE airline_name = %s", (one_way_info[4],))
            result = cursor.fetchone()
            
            if result:
                airline_id = result[0]
            else:
                cursor.execute(
                    "INSERT INTO airlines (airline_name) VALUES (%s) RETURNING airline_id", 
                    (one_way_info[4],))
                connection.commit()
                airline_id = cursor.fetchone()[0]
            
            '''Departure Airplane Type'''
            departure_airplane = scraped_info["Departure Airplane Type"]
            print(f"Inserting departure airplane \"{departure_airplane}\" into database...")
            cursor.execute("SELECT airplane_id FROM airplanes WHERE airplane_type = %s", (departure_airplane,))
            result = cursor.fetchone()
            
            if result:
                departure_airplane_id = result[0]
            else:
                cursor.execute("INSERT INTO airplanes (airplane_type) VALUES (%s) RETURNING airplane_id",
                            (departure_airplane, ))
                connection.commit()
                departure_airplane_id = cursor.fetchone()[0]
                
            '''Arrival Airplane Type'''
            arrival_airplane = scraped_info["Arrival Airplane Type"]
            print(f"Inserting arrival airplane \"{arrival_airplane}\" into database...")
            cursor.execute("SELECT airplane_id FROM airplanes WHERE airplane_type = %s", (arrival_airplane,))
            result = cursor.fetchone()
            
            if result:
                arrival_airplane_id = result[0]
            else:
                cursor.execute("INSERT INTO airplanes (airplane_type) VALUES (%s) RETURNING airplane_id",
                            (arrival_airplane, ))
                connection.commit()
                arrival_airplane_id = cursor.fetchone()[0]
            
            '''Departure\Arrival Airport'''
            print(f"Inserting Departure Airport: \"{one_way_info[5]}\" and \"{user_data[0]}\" into database...")
            cursor.execute("SELECT airport_id FROM airports WHERE airport_name = %s and city = %s", (one_way_info[5],user_data[0], ))
            result = cursor.fetchone()
            
            if result:
                departure_airport_id = result[0]
            else:
                cursor.execute("INSERT INTO airports (airport_name, city) VALUES (%s, %s) RETURNING airport_id",
                            (one_way_info[5], user_data[0], )) # Origin airport as well as city
                connection.commit()
                departure_airport_id = cursor.fetchone()[0]
            
            
            print(f"Inserting Arrival Airport: \"{one_way_info[8]}\" and \"{user_data[1]}\" into database...")
            cursor.execute("SELECT airport_id FROM airports WHERE airport_name = %s and city = %s", (one_way_info[8], user_data[1], ))
            result = cursor.fetchone()
            
            if result:
                arrival_airport_id = result[0]
            else:
                cursor.execute("INSERT INTO airports (airport_name, city) VALUES (%s, %s) RETURNING airport_id",
                                (one_way_info[8], user_data[1], )) # destination airport as well as city
                connection.commit()
                arrival_airport_id = cursor.fetchone()[0]
            
            roundtrip_id = None
            if user_data[-1] == True: # if roundtrip
                flight_direction = "Returning"
                rnd_trip_passengers = 0
                print(f"Inserting \"{cleaned_data[-1]}\" and \"{ttl_passengers}\" into database...")
                cursor.execute("INSERT INTO roundtrips (total_price, num_passengers) VALUES (%s, %s) RETURNING roundtrip_id",
                        (cleaned_data[-1], ttl_passengers, ) )
                connection.commit()
                roundtrip_id = cursor.fetchone()[0]
                
            print(f"Inserting flight features into database...")
            if roundtrip_id:
                cursor.execute(
                    "INSERT INTO flight_features (flight_price, roundtrip_id, flight_direction, num_stops, airline_id, search_date, departure_airport_id, departure_time, departure_date, arrival_airport_id, arrival_time, arrival_date, travel_duration, num_layovers, num_carryon, num_checked, num_adults, num_children, num_infants_in_seat, num_infants_on_lap, seating_class, round_trip, departure_airplane_type_id, arrival_airplane_type_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING flight_id",
                        (one_way_info[0],  roundtrip_id, flight_direction, one_way_info[1], airline_id, user_data[7], departure_airport_id, one_way_info[6],  one_way_info[7], arrival_airport_id, one_way_info[9], one_way_info[10], one_way_info[11], one_way_info[1], one_way_info[2], one_way_info[3], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[8], departure_airplane_id, arrival_airplane_id,)
                        )  
                connection.commit()
            else:
                try:
                    cursor.execute(
                        "INSERT INTO flight_features (flight_price, flight_direction, num_stops, airline_id, search_date, departure_airport_id, departure_time, departure_date, arrival_airport_id, arrival_time, arrival_date, travel_duration, num_layovers, num_carryon, num_checked, num_adults, num_children, num_infants_in_seat, num_infants_on_lap, seating_class, round_trip, departure_airplane_type_id, arrival_airplane_type_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING flight_id",
                            (one_way_info[0], flight_direction, one_way_info[1], airline_id, user_data[7], departure_airport_id, one_way_info[6],  one_way_info[7], arrival_airport_id, one_way_info[9], one_way_info[10], one_way_info[11], one_way_info[1], one_way_info[2], one_way_info[3], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6], user_data[8], departure_airplane_id, arrival_airplane_id,)
                            )  
                except IndexError: 
                    print("Error")
                    exit()
                connection.commit()
                
            flight_id = cursor.fetchone()[0]
                
        connection.commit()
    print("\n\tFinished.")
    closeConnection(connection, cursor)
      
    '''
        insertIntoAirlines()
        insertIntoAirplanes()
        insertIntoAirports()
        insertIntoRoundTrips()
        insertIntoflight_features()
        inserIntoLayovers()
    '''

    
def driver():
    state_caps = ["Montgomery", "Phoenix", "Little Rock", "Sacramento", "Denver", "Hartford", "Dover", "Tallahassee", "Atlanta", "Honolulu", "Boise", "Springfield", "Indianapolis", "Des Moines", "Topeka", "Frankfort", "Baton Rougue", "Augusta", "Boston", "Lansing", "Saint Paul", "Jackson", "Jefferson City", "Helena", "Lincoln", "Carson City", "Concord", "Trenton", "Santa Fe", "Albany", "Raleigh", "Bismarck", "Columbus", "Oklahoma City", "Salem", "Harrisburg", "Providence", "Columbia", "Pierre", "Nashville", "Austin", "Salt Lake City", "Montpelier", "Richmond", "Olympia", "Charleston", "Madison", "Cheyenne"]
    for capitals in state_caps:
        current_date = datetime.now().date()
        URL = "https://www.google.com/travel/explore"
        driver, wait = intialize(URL)
        accessOriginDestination(wait, driver, "BWI ", f"{capitals} ")
        access_Flights(driver)
        extraced_flight_info = retrieveFlightDetails(driver, wait, False)
        
        user_data = ["BWI", f"{capitals}", 1, 0, 0, 0, "Economy", current_date, False]
        pipeline(extraced_flight_info, user_data)
        print("\nComplete.")
        driver.close()
    
   
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
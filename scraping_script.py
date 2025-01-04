from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import spacy
from spacy.matcher import Matcher  



URL = "https://www.google.com/travel/explore"

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
    accessTripLength(wait) # Access Trip-Length entry-button for user
    
    
    # Select the month for user
    first_month_button = driver.find_element(By.CSS_SELECTOR, "span[data-value='1']").find_element(By.CSS_SELECTOR, "button[jsname='LgbsSe']")
    first_month_button.click()
    time.sleep(1)
    second_month_button= driver.find_element(By.CSS_SELECTOR, "span[data-value='2']").find_element(By.CSS_SELECTOR, "button[jsname='LgbsSe']")
    second_month_button.click()
    time.sleep(1)
    third_month_button= driver.find_element(By.CSS_SELECTOR, "span[data-value='3']").find_element(By.CSS_SELECTOR, "button[jsname='LgbsSe']")
    third_month_button.click()
    time.sleep(1)
    fourth_month_button= driver.find_element(By.CSS_SELECTOR, "span[data-value='4']").find_element(By.CSS_SELECTOR, "button[jsname='LgbsSe']")
    fourth_month_button.click()
    time.sleep(1)
    fifth_month_button= driver.find_element(By.CSS_SELECTOR, "span[data-value='5']").find_element(By.CSS_SELECTOR, "button[jsname='LgbsSe']")
    fifth_month_button.click()
    time.sleep(1)
    sixth_month_button= driver.find_element(By.CSS_SELECTOR, "span[data-value='6']").find_element(By.CSS_SELECTOR, "button[jsname='LgbsSe']")
    sixth_month_button.click()
    time.sleep(1)
    all_months_button = driver.find_element(By.CSS_SELECTOR, "span[data-value='0']").find_element(By.CSS_SELECTOR, "button[jsname='LgbsSe']")
    all_months_button.click()
    time.sleep(1)
    
    # Find Trip-Length Div
    trip_duration_div = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Trip duration']")   
    #two_week_button = trip_duration_div.find_element(By.CSS_SELECTOR, "button[jsname='LgbsSe']")
    #two_week_button.click()
    span_text = "2 weeks"  # You can change this to any text you're looking for regarding trip duration (Weekend, 1 week, 2 weeks)
    
    # Find the span element with the text of the week_type
    span = trip_duration_div.find_element(By.XPATH, f".//span[normalize-space(text())='{week_type}']") # span_text
    
    # Access the button element
    button = span.find_element(By.XPATH, "..//..//..//..//button")
    button.click()
    time.sleep(2)
    
    #Click Done Button
    div = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class='ohKsQc']")))
    done_button = div.find_element(By.CSS_SELECTOR, "button[jsname='McfNlf']")
    done_button.click() 
    time.sleep(2) 
    

def accessNumOfPassengers(wait, driver, num_adults, num_children, num_infants_in_seat, num_infants_on_lap):
    '''Retreieve the # of passangers'''
    
    # Number of people going
    # access the number of passengers button
    num_of_passengers_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div[jsname='QqIbod']"))) 
    num_of_passengers_button.click()
    time.sleep(2)
    
    # access the add adult button
    add_adult_button = driver.find_element(By.CSS_SELECTOR, "ul[jsname='nK2kYb']").find_element(By.CSS_SELECTOR, "button[aria-label='Add adult']")
    add_adult_button.click()
    time.sleep(1)
    
    # access the add children button
    add_children_button = driver.find_element(By.CSS_SELECTOR, "ul[jsname='nK2kYb']").find_element(By.CSS_SELECTOR, "button[aria-label='Add child']")
    add_children_button.click()
    time.sleep(1)
    
    # access the add infants in seat button
    add_infants_in_seat_button = driver.find_element(By.CSS_SELECTOR, "ul[jsname='nK2kYb']").find_element(By.CSS_SELECTOR, "button[aria-label='Add infant in seat'")
    add_infants_in_seat_button.click()
    time.sleep(1)
    
    # access the add infants on lap button
    add_infants_on_lap_button = driver.find_element(By.CSS_SELECTOR, "ul[jsname='nK2kYb']").find_element(By.CSS_SELECTOR, "button[aria-label=aria-label='Add infant on lap']")
    add_infants_on_lap_button.click()
    time.sleep(2)
    

def accessSeatingClass(wait, driver, class_type):
    ''' Retrive the Seating Class (Economy, Prem Econ, Business, First) '''
    
    # access the seating class button
    seating_class_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div[jsname='zkxPxd']")))
    seating_class_button.click()
    time.sleep(1)
    # if class_type == "Economy":
    class_type_button = driver.find_element(By.CSS_SELECTOR, "ul[aria-label='Select your preferred seating class.']").find_element(By.CSS_SELECTOR, "li[data-value='2']") # 1 = Economy, 2 = Prem Econ, 3 = Business, 4 = First
    class_type_button.click()
    time.sleep(2)
    
def changeRoundTrip(wait, driver):
    ''' Retrive Round-Trip or One-way '''
    #Click Round-Trip Button
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
    destination = "BWI "
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
    # Scroll the element into view using JavaScript so we can click on the button
    driver.execute_script("arguments[0].scrollIntoView(true);", view_more_flights_button)
    view_more_flights_button.click()
    time.sleep(5)
    
def get_search_results(driver):
    URL = "https://www.google.com/travel/flights/search?tfs=CBwQAhojEgoyMDI1LTAxLTA1agcIARIDQldJcgwIAhIIL20vMDJjbDEaIxIKMjAyNS0wMS0wNmoMCAISCC9tLzAyY2wxcgcIARIDQldJQAFIAXABggELCP___________wGYAQE&tcfs=ChUKCC9tLzA5NGp2GglCYWx0aW1vcmVSBGABeAE"
    driver, wait = intialize(URL) # Initialize the driver and wait objects
    accessSeatingClass(wait, driver, "Prem Econ") # Access the seating class for user
    exit()
    '''View More Flights'''
    view_more_flights_button = driver.find_element(By.XPATH, "//button[@aria-label='View more flights']")
    # Scroll the element into view using JavaScript so we can click on the button
    driver.execute_script("arguments[0].scrollIntoView(true);", view_more_flights_button)
    view_more_flights_button.click()
    time.sleep(5)
    
    all_results = driver.find_elements(By.XPATH, "//ul[@class='Rk10dc']/li")
    randomHash = {}
    
    for result in all_results:
        try:
            aria_label = result.find_element(By.XPATH, ".//div[@class='JMc5Xc']").get_attribute("aria-label")
        except:
            print("")
        if aria_label is not None:
            print(aria_label + "\n")
            # Call NLP function to extract flight information
            doc = nlp(aria_label)
            extractFlightInfo(doc)
            
            
def extractFlightInfo(nlp_doc):
    price_pattern = [
        [{"POS": "NUM"}, {"ORTH": "US"}, {"ORTH": "dollars"}] 
        ]
    num_stops_pattern = [
        [{"POS": "NUM"}, {"LOWER": "stop"}, {"LOWER": "flight"}]
    ]
    
    duration_pattern = [
         [{"TEXT": "Total"}, {"TEXT": "duration"}, {"POS": "NUM"}, {"LOWER": "hr"}, {"POS": "NUM"}, {"LOWER": "min"}]
    ]
    num_layover_pattern = [
        [{"TEXT": "Layover"}, {"TEXT": "("}, {"POS": "NUM"}, {"TEXT": "of"}, {"POS": "NUM"}, {"TEXT": ")"}]
    ]
    
    layover_duration_pattern = [
        [{"POS": "NUM"}, {"LOWER": "hr"}, {"POS": "NUM"}, {"LOWER": "min"}, {"LOWER": "layover"}]
    ]
    
    departure_time_pattern = [
        [
        {"TEXT": "Leaves"}, {"POS": "PROPN", "OP": "+"}, {"POS": "SYM", "OP": "?"}, {"POS": "PROPN", "OP": "+"}, {"TEXT": "Airport"},
        {"LOWER": "at"}, {"POS": "NUM"}, {"IS_SPACE": True, "OP": "*"}, {"LOWER": {"IN": ["am", "pm"]}},
        {"LOWER": "on"}, {"POS": "PROPN"}, {"TEXT": ","},
        {"POS": "PROPN"},{"POS": "NUM"},
        ]
    ]
    
    arrival_time_pattern = [
       [{"TEXT":"arrives"}, {"LOWER":"at"}, {"POS": "PROPN", "OP": "+"},
        {"POS": "SYM", "OP": "?"}, {"TEXT": "Airport"}, {"LOWER":"at"}, {"POS": "NUM"}, {"IS_SPACE": True, "OP": "*"}, 
        {"LOWER": {"IN": ["am", "pm"]}}, {"LOWER": "on"}, {"POS": "PROPN"}, {"TEXT": ","}, {"POS":"PROPN"}, {"POS": "NUM"}]
       ]
    
    layover_duration_pattern = [
        [{"LOWER":"is"}, {"LOWER":"a"}, {"POS": "NUM"}, {"LOWER": "hr"}, {"POS": "NUM"}, {"LOWER": "min"}]
    ]
    
    airline_pattern = [
        [{"LOWER": "with"}, {"POS": "PROPN"}]
    ]
    connecting_airport_pattern = [
        [{"LOWER":"layover"}, {"LOWER": "at"}, {"POS":"PROPN", "OP":"+"},{"POS":{"IN":["PUNCT", "SYM"]}, "OP":"?"}, 
         {"POS":"PROPN", "OP":"+"}, {"TEXT": "Airport"}, {"LOWER": "in"}, {"POS": "PROPN"}]
        ]
    num_of_carryon_pattern = [
        [{"POS": "NUM"}, {"LOWER": "carry"}, {"LOWER":"-"}, {"LOWER":"on"}, {"LOWER": "bags"}]
    ]
    num_of_checked_pattern = [
        [{"POS": "NUM"}, {"LOWER": "checked"}, {"LOWER": "bags"}]
    ]
    
    matcher.add("FLIGHT_PRICE", price_pattern) # correct
    matcher.add("NUM_STOPS", num_stops_pattern) # correct
    matcher.add("FLIGHT_DURATION", duration_pattern) # correct
    matcher.add("NUM_LAYOVERS", num_layover_pattern) # correct
    matcher.add("LAYOVER_DURATION", layover_duration_pattern) # correct
    matcher.add("DEPARTURE_TIME", departure_time_pattern)
    matcher.add("ARRIVAL_TIME", arrival_time_pattern)

    matcher.add("AIRLINE", airline_pattern) # correct
    matcher.add("CONNECTING_AIRPORT", connecting_airport_pattern)
    matcher.add("NUM_CARRYON", num_of_carryon_pattern) # correct
    matcher.add("NUM_CHECKED", num_of_checked_pattern) # correct
    matches = matcher(nlp_doc)
    for _, start, end in matches:
        span = nlp_doc[start:end]
        print(span.text)
        
    # Get round trip or one way from user input

def clean_data(data):
    '''Clean the data'''
    '''Create a pipeline to store into SQL database'''
    
    return

    
def main():

    
    '''
    #Retrieve User Input
    accessSpecificDates(wait, driver, "1/5/2025", "1/10/2025") # Access Specific Dates for user
    accessFlexibleDates(wait, driver, "January", "2 weeks") # Access Flexible Dates for user
    accessNumOfPassengers(wait, driver, 2, 1, 1, 1) # Access the number of passengers for user
    accessSeatingClass(wait, driver, "Prem Econ") # Access the seating class for user
    round_trip = False
    if not round_trip:
        changeRoundTrip(wait, driver) # Access the round trip or one-way for user
    accessOriginDestination(wait, driver, "BWI", "LAX") # Access the origin and destination for user

    
    
    
    
    exit()
    
    '''
    
    
    # NLP Stuff for data scrape
    # Google Flights Flights page
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/travel/flights/search?tfs=CBwQAhojEgoyMDI1LTAxLTA1agcIARIDQldJcgwIAhIIL20vMDJjbDEaIxIKMjAyNS0wMS0wNmoMCAISCC9tLzAyY2wxcgcIARIDQldJQAFIAXABggELCP___________wGYAQE&tfu=EgYIABABGAA&tcfs=ChUKCC9tLzA5NGp2GglCYWx0aW1vcmVSBGABeAE")
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
    

nlp = spacy.load("en_core_web_sm")
matcher = Matcher(nlp.vocab)
main()

# aria-label='Some text' is your best bet for finding elements
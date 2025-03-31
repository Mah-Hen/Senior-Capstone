--CREATE DATABASE Flights;
CREATE TABLE airlines(
	airline_id SERIAL PRIMARY KEY, 
	airline_name VARCHAR(255)
);

CREATE TABLE airplanes(
	airplane_id SERIAL PRIMARY KEY, 
	airplane_type VARCHAR(255)
);

CREATE TABLE airports (
	airport_id SERIAL PRIMARY KEY,
	airport_name VARCHAR(255), 
	city VARCHAR(255) 
);


CREATE TABLE roundtrips(
	roundtrip_id SERIAL PRIMARY KEY, 
	total_price INT,
	num_passengers INT
);
CREATE TABLE flight_features(
	flight_id SERIAL PRIMARY KEY,
	flight_price INT,
	roundtrip_id INT REFERENCES roundtrips(roundtrip_id),
	flight_direction VARCHAR(10) NOT NULL, 
	num_stops INT,
	airline_id INT REFERENCES airlines (airline_id), 
	search_date DATE, 
	departure_airport_id INT REFERENCES airports(airport_id), 
	departure_time TIME, 
	departure_date VARCHAR(50), 
	arrival_airport_id INT REFERENCES airports(airport_id), 
	arrival_time TIME, 
	arrival_date VARCHAR(50), 
	travel_duration INTERVAL, 
	num_layovers INT, 
	--layover_duration VARCHAR(255), 
	--layover_destination VARCHAR(255), 
	num_carryon INT, 
	num_checked INT, 
	num_adults INT, 
	num_children INT, 
	num_infants_in_seat INT,
	num_infants_on_lap INT, 
	seating_class VARCHAR(255), 
	round_trip BOOLEAN,
	departure_airplane_type_id INT REFERENCES airplanes(airplane_id)
	arrival_airplane_type_id INT REFERENCES airplanes(airplane_id)
	 
);

CREATE TABLE layovers(
	layover_id SERIAL PRIMARY KEY, 
	flight_id INT REFERENCES flight_features(flight_id), 
	layover_airport_id INT REFERENCES airports(airport_id),
	layover_duration INTERVAL
);

--DROP DATABASE Flights;
--DROP TABLE flight_features CASCADE;
SELECT * FROM flight_features;

/* Data from scraping the flight status is */
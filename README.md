# Data Scraping Web Visualizer

A comprehensive project for web scraping, PostgreSQL-based data storage, and front-end development to display and interact with collected data.

## Table of Contents
- Project Overview
- Features
- Technologies Used
- Getting Started
- Prerequisites
- Installation
- Project Structure
- Usage
- Running the Scraper
- Database Setup
- Future Front-End Integration
- Contributing
- License
  
## Project Overview
This capstone project uses a Python-based web scraper to collect and store structured data from Google Flights. The data is stored in a PostgreSQL database. Future iterations will include a user-friendly front-end interface to visualize and interact with the data.

## Features
- Web Scraping: Extracts dynamic data from specified websites.
- PostgreSQL Integration: Stores data in a relational database for efficient querying.
- Extensible Design: Planned integration of a front-end for data visualization and interaction.

## Technologies Used
- Python: For web scraping using libraries such as requests, BeautifulSoup, or Selenium.
- PostgreSQL: For relational data storage.
- HTML/CSS/JavaScript (Planned): For the front-end interface.

## Getting Started

### Prerequisites
- Python 3.7+
- PostgreSQL installed and running
- pip for managing Python packages

### Installation
1. Clone the repository:
```
git clone https://github.com/your_username/your_project.git
cd your_project
```
2. Install required Python packages:
```
pip install -r requirements.txt
```
3. Set up the PostgreSQL database:
- Create a database using your PostgreSQL client.
- Update the config.py file with your database credentials.

## Project Structure
```
project_name/
├── scraper/
│   ├── scraper.py          # Web scraping script
│   ├── utils.py            # Helper functions for scraping
│   └── config.py           # Configuration file for database credentials
├── database/
│   ├── schema.sql          # SQL script for setting up the database schema
│   └── db_operations.py    # Python scripts for database interactions
├── frontend/               # (Planned) Front-end development
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```
## Usage
### Running the Scraper
1. Navigate to the scraper directory:
```
cd scraper
```
2. Run the scraping script:
```
python scraper.py
```
### Database Setup
1. Execute the schema file to set up the database:
```
psql -U your_username -d your_database -f database/schema.sql
```
2. Verify the database connection by running the db_operations.py script:
```
python database/db_operations.py
```

### Future Front-End Integration
The front-end development will be added in future iterations. Stay tuned for updates!

## Contributing
Please send me a message before any changes are committed. But yeah, send a fork.

## License
This project is licensed under the MIT License. See the LICENSE file for details.


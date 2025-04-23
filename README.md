# Data Scraping Web Visualizer

A comprehensive project for web scraping flight data, PostgreSQL-based data storage, and front-end development to display and interact with collected data.

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
- Viewing the Dashboard
- Contributing


## Project Overview

This capstone project uses a Python-based web scraper to collect and store structured data from Google Flights. The data is stored in a PostgreSQL database. Where, utilizing PLotly's Dash, a data visualization Dashboard is developed as User-Interface and Experience.

## Features

- Web Scraping: Extracts dynamic data from specified websites.
- PostgreSQL Integration: Stores data in a relational database for efficient querying.
- Dashboard Design: Integration of Plotly's Dash for data visualization and interaction.

## Technologies Used

- Python: For web scraping using Selenium.
- SpaCy: For natural lanugage parsing
- PostgreSQL: For relational data storage.
- Python's Dash: For the front-end interface.

## Getting Started

### Prerequisites

- Python 3.7+
- PostgreSQL installed and running
- pip for managing Python packages

### Installation

1. Clone the repository:

```
git clone https://github.com/Mah-Hen/Senior-Capstone.git
cd Senior-Capstone
```

2. Create Virtual Environment:
   
```
python -m venv <directory>
```

4. Activate Virutal Environment:
   
```
# In cmd.exe
venv\Scripts\activate.bat
# In PowerShell
venv\Scripts\Activate.ps1
# In Linux
source myvenv/bin/activate
```

5. Install required Python packages:

```
pip install -r requirements.txt
```

6. (OPTIONAL) Set up the PostgreSQL database:

- Create a database using your PostgreSQL client.
- Update your system environment file with your database credentials.

## Project Structure

```
project_name/
├── scraper/
│   ├── scraper.py          # Web scraping script
├── database/
│   ├── schema.sql          # SQL script for setting up the database schema
│   └── data_processing.py    # Python scripts for database interactions
├── frontend/               # Python's Dash Front-end development
│    ├── pages          # Dash HTML Pages
│    └── app.py    # Dash's main app control
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Usage

### Running the Scraper

1. Navigate to the 'scraper' directory:

```
cd scraper
```

2. Run the scraping script:

```
python3 scraper.py
```
### Viewing the Dashboard

1. Navigate to the 'frontend' directory:
```
cd frontend
```

2. Run the Dashboard App script:
```
python3 app.py
```

3. Click on the URL to view Dashboard
```
Dash is running on http://localhost:8050/

 * Serving Flask app 'app'
 * Debug mode: on
```

## Contributing

Please send me a message before any changes are committed. But yeah, send a fork.

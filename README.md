# This is an application handling data about the titanic's passengers

It allows you to:
- Upload a csv file with the correct format
- Query the data with various filters
  
To make things easier to tests locally, some technical choices were made, the main one being that the database is a file based sqlite database.

## Features
- **Upload CSV File**: Upload a CSV file containing Titanic passenger data and store it in the database.
- **Retrieve Passengers**: Fetch passenger data.
- **Delete Passengers**: Delete all passenger records.
- **Filter Support**: Query passengers by survival status, class, name, gender, age, ticket number, and port of embarkation.

## Setup

### Activate the virtual environment:

`source ./.venv/Scripts/activate`

### Install dependencies

`pip install -r requirements.txt`

### Run the application

`fastapi dev main.py`

### Run the tests

`pytest`

Some example files are provided in the resources folder which also contains the postman collection:
- empty.csv, an empty csv file
- train.csv, a valid file with records
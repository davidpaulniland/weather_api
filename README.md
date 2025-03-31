# Weather API

**Python version: 3.11.5**

### Create virtual env
python3 -m venv venv
source venv/bin/activate

### Install dependencies
pip install -r requirements.txt


### FastAPI app with auto-reload
uvicorn app.main:app --reload

### Manual run
python3 -m app.main


### Run tests
pytest tests/tests.py



### Notes

This app stores data in a JSON file (sensors.json) for simplicity.

The API is RESTful and accepts POST and GET requests for sensor data.

Input validation and error handling are included:

Date ranges must be between 1 and 31 days

Only supported stat types are allowed

Unit tests are provided for key functionality
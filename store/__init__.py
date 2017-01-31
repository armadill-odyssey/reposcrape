import datetime
import json
from pprint import pprint

# from pymongo import MongoClient
# client = MongoClient('mongodb://localhost:27017/')
# db = client.log

def saveToFile(data):
    """
    Write data to json file
    """
    today = str(datetime.datetime.now().date())
    # Write response to JSON file
    postingsFile = "data/" + today + '.github.json'

    with open(postingsFile, 'w') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=2)

    outfile.close()

def save(data):
    """
    Save data to mongodb
    """

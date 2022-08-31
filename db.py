import os
from xml.etree.ElementInclude import include
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint

### Connecting to MongoDB Atlas [Video Reference: https://www.youtube.com/watch?v=UpsZDGutpZc&t=1s]
DB_PASSWORD = os.environ.get("MONGODB_PWD") # Retrive the stored DB_PASSWORD from the local .env 
DB_USERNAME = os.environ.get("MONGODB_USR") # Retrive the stored DB_USERNAME from the local .env 

connection_string = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@aatlascluster.setbxte.mongodb.net/?retryWrites=true&w=majority" # MongoDB Connection URI
client = MongoClient(connection_string)
TAGAR_DB = client["TAGAR"]  # Select the database to use from MongoDB
collections = TAGAR_DB.list_collection_names();

### Inserting Data
def insert_record(DB_Collection, JSONdocument):
    DB_Collection.insert_one(JSONdocument)

### Find Data
def find_all_cases():
    """
    > This function returns all cases in the database
    :return: A list of all cases in the database.
    """
    cases = TAGAR_DB.Case.find()

    return cases

def find_one_case(case_obj_id):
    """
    It takes a case object id and returns the case object
    
    :param case_obj_id: the ObjectId of the case you want to find
    :return: A dictionary of the case.
    """

    from bson.objectid import ObjectId
    _id = ObjectId(case_obj_id)

    case = TAGAR_DB.Case.find_one({"_id":_id})

    return case

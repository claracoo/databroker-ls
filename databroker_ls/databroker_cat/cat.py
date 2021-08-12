from databroker_ls.command_line import get_current_catalog
from databroker import catalog

import databroker_ls
from os import path
from databroker_ls.args import get_args
from databroker_ls.databroker_cat.mongo_query import output_bluesky_docs

import yaml
import pprint
import pymongo

def make_doc_list(documents, key):
    """
        This function compiles the bluesky documents from the dictionary produced in mongo_query.py of a certain key 
        (ie all event docs) and places them in one string    
        This is largely for formatting.

        documents - is the output of a yml file read
        key - is the type of bluedky docs we are looking for
    """
    doc_list = [] # array where docs are stored
    for doc in documents[key].values():
                doc_list.append(doc) # get documents of key and append to our storage list
    return doc_list

def get_catalog():
    """
        This function accesses the file databroker.command_line.py to get the current catalog we are using.
        If the catalog is not specified, that script will take care of asking the user to select a catalog.
    """
    path_prefix = path.split(databroker_ls.__path__[0])[0]  # get path where catalog is stored
    file = path.join(path_prefix, "conf_catalog.yml") # file  where catalog is stored
    currentCatalog = catalog[get_current_catalog(file)] # get from yaml file the catalog we want (function in command_line.py)
    return currentCatalog

def print_docs(documents):
    """
        Does the actual printing for the bluesky documents.
        Uses pretty print, but better formatting should be used.

        bluesky_doc - is the file from which we are reading the data, will be a yml file
    """
    pp = pprint.PrettyPrinter(indent=4) # how indented each dictionary should be
    print("start: ")
    pp.pprint(documents["start"]) # get start doc
    print("descriptors: ")
    pp.pprint(make_doc_list(documents, "descriptor")) # get multiple descriptor docs
    print("events: ")
    pp.pprint(make_doc_list(documents, "event")) # get multiple event docs
    print("resources: ")
    pp.pprint(make_doc_list(documents, "resource")) # get multiple resource docs
    print("data: ")
    pp.pprint(make_doc_list(documents, "datum")) # get multiple datum docs
    print("stop: ")
    pp.pprint(documents["stop"]) # get stop doc

def get_uid():
    """
        This function gets the uuid of the run in question:
        The user is able to input uids, scan ids, or backwards index: this function finds the correct uid in catalog.
        If the run is not valid, it will prompt the user.
    """
    run = get_args().run # get their input (args.py is in databroker_ls)
    if run[0] == "-": # the input is always a string, we need to check if they input a backwards index
        run = int(run) # backwards indices treated as ints
    try: # if the run exists and is in the catalog, we can use their input
        get_catalog()[run]
    except LookupError: # if specified run not in catalog, prompt user
        print("This was not a valid run, try 'db-ls' to see the possible runs.")
        return None # return a lack of uid, MUST CHECK FOR THIS
    return get_catalog()[run].metadata["start"]["uid"] # return successful uid

def is_connected_to_mongo():
    """
        Make sure user is connected to mongo; returns True if connected, False otherwise.
        Check below url to make sure you are looking for the right port.
    """
    maxSevSelDelay = 1 # how long to spend looking for mongo
    try: # make sure this address is running
        url = "mongodb://127.0.0.1:27017" # standard mongo port
        client = pymongo.MongoClient(url, serverSelectionTimeoutMS=maxSevSelDelay) # check the url for specified amt of time
        client.admin.command("serverStatus") # connect via serverStatus (will not cause error if connected)
    except pymongo.errors.ServerSelectionTimeoutError as err: # error if serverStatus does not go through
            return False # not connected
    return True # connected

def main():
    """
        Main function for db-cat (see setup.py).
        If the user is connected to mongo and inputs a usable uid, will connect and print from database
    """
    if is_connected_to_mongo(): # makes sure we are connected to mongo
        uid = get_uid() # takes user input and converts to uid (will be None if invalid)
        if uid != None: # if the uid is valid...
            bluesky_doc = output_bluesky_docs(uid) # get the bluesky documents into one printable dictionary
            print_docs(bluesky_doc) # print what was stored in dict from database
    else: # what the user sees if not hooked up to mongo
        print("You are not connected to mongo.")
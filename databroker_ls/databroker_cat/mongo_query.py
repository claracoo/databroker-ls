import pymongo
import yaml
from os import path
import pprint
from collections import OrderedDict
import argparse

def get_inner_outer_data(mydb, uid, pointer_key, pointer_query_key, info_key, info_id_key):
    """
        This function is meant to handle descriptors and their events and resources and their data documents.
        Both of these contain pointers to address structures, so they are combined in the same function

        mydb - is the database from which we are drawing from (ar for resource and datum docs, md for descriptor and event docs)
        uid - resource and descriptors have uids that are used to identify what their associated datum and event docs are, respectively
        pointer_key - is the collection name in the database for the resources/descriptors
        pointer_query_key - is the key in the key value pair for which we are searching the database
            we want to look for every datum that has a key value pair of "resource": some uid
            we want to look for every event that has a key value pair of "descriptor": some uid
        info_key - is the collection name in the database for the data/events
        info_id_key - how I chose to label the individual events/data: this variable gets the uid
            <collection name>.<uid> <-- which is gotten from the info_id_key
    """
    run_start_query = {'run_start': str(uid)} # key all the descriptors or resources associated with a particular start doc
    info = {} # where we hold all events or data
    pointers = {} # where we hold all descriptors or resources
    pointer_list = list(mydb[pointer_key].find(run_start_query)) # get all descriptors or resources
    for pointer in pointer_list: # for each descriptor or resource:
        pointer.pop("_id") # get rid of the database id (this is not useful to be printed to the user)
        key = str(pointer_query_key) + "_" + str(pointer["uid"]) # label it something more useful to divide the descriptors/resources visuall for user
        pointers[key] = pointer # add to our storage list
        pointer_query = {pointer_query_key: pointer['uid']} # key all the events or data associated with a particular descriptor/resource
        info_list = list(mydb[info_key].find(pointer_query)) # get all the events or data associated with a particular descriptor/resourc
        for elem in info_list: # for each event or datum
            elem.pop("_id") # get rid of the database id (this is not useful to be printed to the user)
            key = str(info_key) + str(elem[info_id_key]) # label it something more useful to divide the events/data visuall for user
            info[key] = elem # add to our storage list
    return pointers, info # output the descriptors/resources separately from the events/data

def get_start(mydb, uid):
    """
        Get start document info.

        mydb - is the database from which we are drawing from (will almost always be md for start)
        uid - which run are we getting, indirectly inputted by user
    """
    start_uid_query = {'uid': str(uid)} # key to getting all (should only be one) start docs with that uid
    start = list(mydb["run_start"].find(start_uid_query))[0] # we will get a list of one
    start.pop("_id") # get rid of the database id (this is not useful to be printed to the user)
    return start

def get_stop(mydb, uid):
    """
    Get start document info.

    mydb - is the database from which we are drawing from (will almost always be md for stop)
    uid - is the start doc's databse id
    """
    run_start_query = {'run_start': str(uid)} # key to getting all (should only be one) stop docs associated with that start doc id
    stop = list(mydb["run_stop"].find(run_start_query))[0] # get the stop doc
    stop.pop("_id") # get rid of the database id (this is not useful to be printed to the user)
    return stop

def get_all_docs(md_db, ar_db, uid):
    """
        This compiles all the database documents into one dictionary we can save in a dictionary.
    """
    data = {}
    data["start"] = get_start(md_db, uid)
    data["descriptor"] = get_inner_outer_data(md_db, uid, "event_descriptor", "descriptor", "event", "uid")[0]
    data["event"] = get_inner_outer_data(md_db, uid, "event_descriptor", "descriptor", "event", "uid")[1]
    data["resource"] = get_inner_outer_data(ar_db, uid, "resource", "resource", "datum", "datum_id")[0]
    data["datum"] = get_inner_outer_data(ar_db, uid, "resource", "resource", "datum", "datum_id")[1]
    data["stop"] = get_stop(md_db, uid)
    return data

def output_bluesky_docs(uid):
    """
        This function connects to the 2 databases ar and md and outputs a dictionary with all the database info extracted.

        uid - this is the uid of the run the user wants to see.
    """
    myclient = pymongo.MongoClient("mongodb://localhost:27017/") # connect to mongo at the standard port
    md_db = myclient["md"] # get db containing start, descriptors, events, and stop docs
    ar_db = myclient["ar"] # get db containing resource and datum docs
    return get_all_docs(md_db, ar_db, uid) # place into one dictionary
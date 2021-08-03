import pymongo
import yaml
from os import path
import pprint
from collections import OrderedDict
import argparse

def output_bluesky_docs(uid):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["md"]
    mycol = mydb["run_start"]

    file_prefix = "bluesky_doc_"
    file_suffix = ".yml"
    filename = file_prefix + str(uid) + file_suffix

    start_uid_query = {'uid': str(uid)}
    start = list(mydb["run_start"].find(start_uid_query))[0]
    start.pop("_id")

    run_start_query = {'run_start': str(uid)}

    descriptor = list(mydb["event_descriptor"].find(run_start_query))[0]
    descriptor_query = {'descriptor': str(descriptor["uid"])}
    descriptor.pop("_id")

    event_list = list(mydb["event"].find(descriptor_query))
    events = {}
    for event in event_list:
        event.pop("_id")
        key = "event_" + str(event["uid"])
        events[key] = event

    stop = list(mydb["run_stop"].find(run_start_query))[0]
    stop.pop("_id")

    data = {}
    data["start"] = start
    data["descriptor"] = descriptor
    data["event"] = events
    data["stop"] = stop

    if not path.exists(
        filename
    ):  # if the file does not exist at all, we will want to create it
        open(filename, "x+")
    with open(filename, "w+") as f:  # open file to write there
        yaml.dump(data, f)  # put the key value pair in the yml file
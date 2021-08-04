import pymongo
import yaml
from os import path
import pprint
from collections import OrderedDict
import argparse

def get_inner_outer_data(mydb, uid, pointer_key, pointer_query_key, info_key, info_id_key):
    run_start_query = {'run_start': str(uid)}
    info = {}
    pointers = {}
    pointer_list = list(mydb[pointer_key].find(run_start_query))
    for pointer in pointer_list:
        pointer.pop("_id")
        key = str(pointer_query_key) + "_" + str(pointer["uid"])
        pointers[key] = pointer
        pointer_query = {pointer_query_key: pointer['uid']}
        info_list = list(mydb[info_key].find(pointer_query))
        for elem in info_list:
            elem.pop("_id")
            key = str(info_key) + str(elem[info_id_key])
            info[key] = elem
    return pointers, info

def get_start(mydb, uid):
    start_uid_query = {'uid': str(uid)}
    start = list(mydb["run_start"].find(start_uid_query))[0]
    start.pop("_id")
    return start

def get_stop(mydb, uid):
    run_start_query = {'run_start': str(uid)}
    stop = list(mydb["run_stop"].find(run_start_query))[0]
    stop.pop("_id")
    return stop

def get_all_docs(md_db, ar_db, uid):
    data = {}
    data["start"] = get_start(md_db, uid)
    data["descriptor"] = get_inner_outer_data(md_db, uid, "event_descriptor", "descriptor", "event", "uid")[0]
    data["event"] = get_inner_outer_data(md_db, uid, "event_descriptor", "descriptor", "event", "uid")[1]
    data["resource"] = get_inner_outer_data(ar_db, uid, "resource", "resource", "datum", "datum_id")[0]
    data["datum"] = get_inner_outer_data(ar_db, uid, "resource", "resource", "datum", "datum_id")[1]
    data["stop"] = get_stop(md_db, uid)
    return data

def output_bluesky_docs(uid):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    md_db = myclient["md"]
    ar_db = myclient["ar"]

    file_prefix = "bluesky_doc_"
    file_suffix = ".yml"
    filename = file_prefix + str(uid) + file_suffix

    if not path.exists(filename):  # if the file does not exist at all, we will want to create it
        open(filename, "x+")
    with open(filename, "w+") as f:  # open file to write there
        yaml.dump(get_all_docs(md_db, ar_db, uid), f)  # put the key value pair in the yml file
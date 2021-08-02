import pymongo
import yaml
from os import path
import pprint
from collections import OrderedDict
import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u",
        "--uid",
        help="Supply a uid",
        type=str,
        dest="uid",
    )

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

    event = list(mydb["event"].find(descriptor_query))[0]
    event.pop("_id")

    stop = list(mydb["run_stop"].find(run_start_query))[0]
    stop.pop("_id")

    #otherdb = myclient["ar"]
    #resource = otherdb["resource"].find(myquery)
    #datum = otherdb["datum"].find(myquery)

    data = {}
    data["start"] = start
    data["descriptor"] = descriptor
    data["event"] = event
    data["stop"] = stop

    if not path.exists(
        filename
    ):  # if the file does not exist at all, we will want to create it
        open(filename, "x+")
    with open(filename, "w+") as f:  # open file to write there
        yaml.dump(data, f)  # put the key value pair in the yml file


def main():
    uid = "6834f071-7fef-4b01-9bc5-eb60790ae641"
    output_bluesky_docs(uid)


if __name__ == "__main__":
    main()

from databroker_ls.command_line import get_current_catalog
from databroker import catalog

import databroker_ls
from os import path
from databroker_ls.args import get_args
from databroker_ls.databroker_cat.mongo_query import output_bluesky_docs

import yaml
import pprint

def make_doc_list(documents, key):
    doc_list = []
    for doc in documents[key].values():
                doc_list.append(doc)
    return str(doc_list)

def get_catalog():
    path_prefix = path.split(databroker_ls.__path__[0])[0]
    file = path.join(path_prefix, "conf_catalog.yml")
    currentCatalog = catalog[get_current_catalog(file)]
    return currentCatalog

def print_docs(bluesky_doc):
    pp = pprint.PrettyPrinter(indent=4)
    if path.exists(bluesky_doc):  # if the file does not exist at all, we will want to create it
        with open(bluesky_doc, "r+") as f:  # open file to write there
            documents = yaml.full_load(f)  # put the key value pair in the yml file
            pp.pprint("start: " + str(documents["start"]))
            pp.pprint("descriptors: " + make_doc_list(documents, "descriptor"))
            pp.pprint("events: " + make_doc_list(documents, "event"))
            pp.pprint("resources: " + make_doc_list(documents, "resource"))
            pp.pprint("data: " + make_doc_list(documents, "datum"))
            pp.pprint("stop: " + str(documents["stop"]))

def get_uid():
    run = get_args().run
    if run[0] == "-":
        run = int(run)
    uid = get_catalog()[run].metadata["start"]["uid"]
    return uid

def main():
    uid = get_uid()
    output_bluesky_docs(uid)
    bluesky_doc = "bluesky_doc_" + str(uid) + ".yml"
    print_docs(bluesky_doc)
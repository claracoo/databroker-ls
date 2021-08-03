from databroker_ls.command_line import get_current_catalog
from databroker import catalog

import databroker_ls
from os import path
from databroker_ls.args import get_args
from databroker_ls.databroker_cat.mongo_query import output_bluesky_docs

import yaml
import pprint

path_prefix = path.split(databroker_ls.__path__[0])[0]
file = path.join(path_prefix, "conf_catalog.yml")
pp = pprint.PrettyPrinter(indent=4)

def main():
    currentCatalog = catalog[get_current_catalog(file)]
    run = get_args().run
    if run[0] == "-":
        run = int(run)
    uid = currentCatalog[run].metadata["start"]["uid"]
    output_bluesky_docs(uid)
    bluesky_doc = "bluesky_doc_" + str(uid) + ".yml"
    if path.exists(
        bluesky_doc
    ):  # if the file does not exist at all, we will want to create it
        with open(bluesky_doc, "r+") as f:  # open file to write there
            documents = yaml.full_load(f)  # put the key value pair in the yml file
            event_list = []
            for event in documents["event"].values():
                event_list.append(event)
            pp.pprint("start: " + str(documents["start"]))
            pp.pprint("descriptor: " + str(documents["descriptor"]))
            pp.pprint("events: " + str(event_list))
            pp.pprint("stop: " + str(documents["stop"]))
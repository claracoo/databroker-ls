# from pynput import keyboard
# from pynput.keyboard import Key, Controller

from databroker_ls.ls import ls

from databroker import catalog

from databroker_ls.args import get_args
from databroker_ls.catalog import SpecifiedCatalog

import os.path
from os import path

import yaml

"""
This file is a script to actually make the lines load dynamically
"""


file = "../conf_catalog.yml"


def format_printing(data, object):

    """
    This is where the actual printing format happens,
    so that we can gather the data in a different point
    """

    for i in range(len(data[0])):
        index = "     "
        if get_args().index:
            index = "{message: <{width}}".format(
                message=object.UUIDtoIndex[data[0][i][2][:8]], width=5
            )
        print(index, data[0][i][0], "   ", data[0][i][1], "   ", data[0][i][2])
    if data[1] == "exit":
        # this was from qt.py, means that the data array is empty
        print(
            "No more data in this catalog, exiting..."
        )  # dot dot dot is important because there is a wait time
        return False  # this kicks us out of the listing state
    else:
        print(data[1])  # reminds user of what to do next


def check_for_yaml(filename):
    """ "
    This function checks if the yaml file meets our requirements
    for using the file as our default value:
        1. the file exists
        2. the file contains the key 'catalog_name'
        3. the correct key name is matched with an actual catalog
    """
    empty = ""  # we want to have 2 arguments returned for consistency in case we check check_for_yaml()[1], so this empty string acts as a safety, so it does not segfault
    if not path.exists(
        filename
    ):  # if the file does not exist at all, we will want to create it
        open(filename, "x+")
        return False, empty  # false means the yaml does not meet our requirements
    else:  # even if it does exist, we need it to have a beamline at the key "catalog_name"
        with open(filename, "r") as f:  # open the yaml file we now know exists
            documents = yaml.full_load(f)  # load the contents
            if documents is not None:
                for key, value in documents.items():
                    if (
                        key == "catalog_name"
                        and documents[key] != ""
                        and documents[key].strip("'").strip('"') in list(catalog)
                    ):  # if the key exists and the value is in the possible catalogs
                        return (
                            True,
                            value,
                        )  # the file does match the necessary requirements, so we return true and the current beamline
        return (
            False,
            empty,
        )  # if we reach this condition, it means the file existed but either did not have the key or the key was matched with an empty or non beamline value


def get_current_catalog(filename):
    """
        This function sets and/or gets the catalog the user wants to use.
        If the user manually enters one by using '--catalog [some catalog name]',
        then we can set that as the catalog. We then check if they already have a
        default set. If they do, we use that. The last option is to ask the user
        to set their default.
    """
    currentCatalog = (
        get_args().catalog
    )  # if they manually set a catalog that should have priority
    specifiedCatalog = SpecifiedCatalog()  # just in case create a catalog class
    if (
        currentCatalog == ""
    ):  # if we go to check the manually set catalog, and there is none, then we either need to use the default or prompt the user
        req = check_for_yaml(filename)
        if req[
            0
        ]:  #  if the file both exists and has something at the key "catalog_name", then we can just use this as a default
            currentCatalog = req[
                1
            ]  # we set the catalog (and the backup listing in the catalog class) to be the listed default from the yaml file
        else:  # if either the file does not exist, or the "catalog_name" key is empty, we need to ask the user to set this
            with open(filename) as f:  # open yaml file
                specifiedCatalog.query_for_catalog(default=list(catalog)[0])  # this runs the script from catalog.py to prompt the user for their default choice
                specifiedCatalog.change_default_catalog(
                    filename,
                    specifiedCatalog.currentCatalog
                )  # update the yaml file to house the default
                currentCatalog = (
                    specifiedCatalog.currentCatalog
                )  # set the catalog choice
    return currentCatalog


def set_default(filename):
    changing_catalog = get_args().updateDefault  # get what is stored in the argument for updateDefault
    if changing_catalog in list(catalog):  # don't update it to a catalog that we cannot access
        specifiedCatalog = SpecifiedCatalog()  # get the catalog class
        if not path.exists(
                filename
        ):  # if the file does not exist at all, we will want to create it
            open(filename, "x+")  # create it
        specifiedCatalog.change_default_catalog(filename, changing_catalog)  # change the catalog in the conf file
    else:
        with open(filename, "r") as f:  # open the yaml file we now know exists
            documents = yaml.full_load(f)  # load the contents
            # explanation to the user that the catalog they picked won't work
            print(f"\nThe specified catalog was not available. The available catalogs are: \n{list(catalog)}\nWe will load data from the current default catalog: \n {documents['catalog_name']}\n")


def main():
    if get_args().updateDefault:  # if this argument is there, we need to update the default catalog
        set_default(file)
    currentCatalog = get_current_catalog(
        file
    )  # get the catalog, either entered, default, or prompt for new default
    print(f"Loading the \'{currentCatalog}\' Catalog...")  # remind the user what the current catalog they're using is
    number = 0  # this is used in the ls class for how many runs should be shown. If it stays at 0, all runs will be shown
    if get_args().head:  # if they only want to see the head (most recent)
        number = get_args().number  # we will give the ls class the positive number (default is 10 but, they can specify)
    if get_args().tail:  # if they only want to see the tail (most distant)
        number = -1 * get_args().number  # we will give the ls class the negative number (default is -10 but, they can specify)
    object = ls(
        catalog=catalog[currentCatalog],  # default or specified
        fullUID=get_args().all,  # special case where we want to see the whole id
        reverse=get_args().reverse,  # puts them in reverse order
        number=number,  # tells us how many and if at the end, beginning or all of them
    )  # instantiate new ls object
    print("     Starting Time          Scan ID      UUID")  # titles for our columns
    data = (
        object.myOwnPrinting()
    )  # first time we access data (no user actions necessary after command)
    format_printing(data, object)


if __name__ == "__main__":
    main()

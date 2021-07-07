#!/usr/bin/env python3
"""tests for hello.py"""

import os
import sys
from subprocess import getstatusoutput, getoutput

import numpy as np
import pytest

from bluesky_live.run_builder import RunBuilder

import databroker
from databroker_ls.ls import ls

from databroker_ls.catalog import SpecifiedCatalog
from databroker_ls.command_line import check_for_yaml, get_current_catalog
import yaml

import re

from random import randint, choice, sample
import string

catalog = databroker.v2.temp()

prg = "/Users/claracook/Desktop/test/databroker-ls/databroker_ls/stupid-ls.py"


# --------------------------------------------------
def test_exists():
    """exists"""

    assert os.path.isfile(prg)


# --------------------------------------------------
def test_runnable():
    """Runs using python3"""

    out = getoutput(f"python3 {prg}")
    assert out.strip() != "Hello, World!"


# --------------------------------------------------
def random_char(y):
    return "".join(choice(string.ascii_letters) for x in range(y))


def place_data(numDataPts):
    sampleNames = [random_char(2) for x in range(numDataPts)]
    for i in range(numDataPts):
        with RunBuilder(
            metadata={"sample": sampleNames[i], "scan_id": randint(10000, 99999)}
        ) as builder:
            builder.add_stream("primary", data={"x": [1, 2, 3], "y": [10, 20, 30]})
            builder.add_stream("baseline", data={"A": [-1, -1], "B": [250, 250]})
        run = builder.get_run()
        for name, doc in run.documents(fill="yes"):
            catalog.v1.insert(name, doc)


def removeEmptyStrs(arr):
    while "" in arr:
        arr.remove("")
    return arr


def joinDateAndTime(arr):
    arr[0] = arr[0] + " " + arr[1]
    arr.pop(1)
    return arr


def test_place_data():
    numDataPoints = 20
    place_data(numDataPoints)
    object = ls(catalog=catalog, fullUID=True, reverse=False, number=numDataPoints)
    spaced = object.myOwnPrinting()[0]
    for i in range(numDataPoints):
        assert object.toReadableDate(
            catalog[spaced[i][2]].metadata["start"]["time"]
        ) == str(spaced[i][0])
        assert str(catalog[spaced[i][2]].metadata["start"]["scan_id"]) == str(
            spaced[i][1]
        )
        assert catalog[spaced[i][2]].metadata["start"]["uid"] == str(spaced[i][2])


def test_check_for_yaml():
    filename = "./conf_catalog.yml"
    assert check_for_yaml(filename)[0] is True  # this should work because it is already set up on my machine
    assert check_for_yaml(filename)[1] in list(databroker.catalog)
    filename = "./non_existent_file.yml"
    assert check_for_yaml(filename)[0] is False  # this does not yet exist, but will be created here
    assert check_for_yaml(filename)[0] is False  # just created but bad formatting (makefile will remove for next test run)

    # check to make sure if the file exists but has the wrong things
    data = {"stupid": "stupid"}
    with open(filename, "w+") as f:  # open file to write there
        yaml.dump(data, f)  # put the key value pair in the yml file
    assert check_for_yaml(filename)[0] is False
    data = {"empty": ""}
    with open(filename, "w+") as f:  # open file to write there
        yaml.dump(data, f)  # put the key value pair in the yml file
    assert check_for_yaml(filename)[0] is False
    data = {"catalog_name": ""}
    with open(filename, "w+") as f:  # open file to write there
        yaml.dump(data, f)  # put the key value pair in the yml file
    assert check_for_yaml(filename)[0] is False
    data = {"catalog_name": "wrong thing"}
    with open(filename, "w+") as f:  # open file to write there
        yaml.dump(data, f)  # put the key value pair in the yml file
    assert check_for_yaml(filename)[0] is False


def test_change_default_catalog():
    filename = "./test.yml"
    open(filename, "x+")
    data = {"catalog_name": "wrong thing"}
    with open(filename, "w+") as f:  # open file to write there
        yaml.dump(data, f)  # put the key value pair in the yml file
    specifiedCatalog = SpecifiedCatalog()
    specifiedCatalog.currentCatalog = "bluesky-tutorial-RSOXS"
    specifiedCatalog.change_default_catalog(filename, specifiedCatalog.currentCatalog)
    with open(filename, "r") as f:  # open the yaml file we now know exists
        documents = yaml.full_load(f)  # load the contents
        assert documents["catalog_name"] == "bluesky-tutorial-RSOXS"


def test_query_for_catalog():
    specifiedCatalog = SpecifiedCatalog()
    expected = "bluesky-tutorial-BMM"
    print("\ninput: JUST HIT ENTER")
    print("LOOK HERE", list(databroker.catalog))
    specifiedCatalog.query_for_catalog(default=list(databroker.catalog)[0])
    assert expected == specifiedCatalog.currentCatalog

    expected = "bluesky-tutorial-RSOXS"
    print("\ninput: 'bluesky-tutorial-RSOXS'")
    specifiedCatalog.query_for_catalog()
    assert expected == specifiedCatalog.currentCatalog

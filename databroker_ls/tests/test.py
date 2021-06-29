#!/usr/bin/env python3
"""tests for hello.py"""

import os
from subprocess import getstatusoutput, getoutput

import msgpack
import numpy as np
import pytest

from bluesky import RunEngine
from bluesky.plans import count
from ophyd.sim import det

from bluesky.plans import count
from bluesky.simulators import summarize_plan
from bluesky_live.run_builder import RunBuilder
from bluesky_live.run_builder import build_simple_run

import databroker
import databroker.tutorial_utils
import suitcase.msgpack
from databroker_ls.qt import ls

from databroker._drivers.msgpack import BlueskyMsgpackCatalog

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
    object = ls(catalog=catalog, fullUID=False)
    spaced = object.myOwnPrinting()[0]
    for i in range(numDataPoints):
        assert object.toReadableDate(
            catalog[spaced[i][2]].metadata["start"]["time"]
        ) == str(spaced[i][0])
        assert str(catalog[spaced[i][2]].metadata["start"]["scan_id"]) == str(
            spaced[i][1]
        )
        assert catalog[spaced[i][2]].metadata["start"]["uid"][:8] == str(spaced[i][2])

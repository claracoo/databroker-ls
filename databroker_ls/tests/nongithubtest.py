#!/usr/bin/env python3
"""tests for hello.py"""

import os.path
from os import path
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

prg = "/Users/claracook/Desktop/test/databroker-ls/databroker_ls/ls.py"


# --------------------------------------------------
def test_exists():
    """exists"""

    assert os.path.isfile(prg)


# --------------------------------------------------
def test_head():
    """more than two items"""

    arg = '"--head"'
    out = getoutput(f'db-ls --head')
    print(out)
    expected = ("""Loading the 'bluesky-tutorial-RSOXS' Catalog...\n     Starting Time          Scan ID      UUID\n      2019-11-17 04:28:56     6959     777b44ae""")
    print(expected)
    assert out.strip() == expected


# --------------------------------------------------
def test_query_for_catalog():
    specifiedCatalog = SpecifiedCatalog()
    expected = "bluesky-tutorial-BMM"
    print("\ninput: JUST HIT ENTER")
    print("LOOK HERE", list(databroker.catalog))
    specifiedCatalog.query_for_catalog(default=list(databroker.catalog)[0])
    assert expected == specifiedCatalog.currentCatalog

    expected = "bluesky-tutorial-RSOXS"
    print("\ninput: 'bluesky-tutorial-RSOXS'")
    specifiedCatalog.query_for_catalog(default=list(databroker.catalog)[0])
    assert expected == specifiedCatalog.currentCatalog

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
def arg_testing(prompt, expected):
    out = getoutput(prompt)
    print(out)
    expected = (expected)
    print(expected)
    assert out.strip() == expected


def test_head():
    prompt = f'db-ls --head --catalog bluesky-tutorial-RSOXS'
    expected = """Loading the 'bluesky-tutorial-RSOXS' Catalog...\n     Starting Time          Scan ID      UUID\n      2019-11-17 04:28:56     6959     777b44ae"""
    arg_testing(prompt, expected)
    prompt = f'db-ls --head --catalog bluesky-tutorial-BMM --number 2'
    expected = """Loading the 'bluesky-tutorial-BMM' Catalog...\n     Starting Time          Scan ID      UUID\n      2021-06-24 18:48:22     64366     9e36935f\n      2021-06-24 18:41:37     42085     c5b4ca9b"""
    arg_testing(prompt, expected)
    prompt = f'db-ls --head --catalog bluesky-tutorial-BMM --number -2'
    arg_testing(prompt, expected)
    prompt = f'db-ls --catalog bluesky-tutorial-BMM --number 2'
    arg_testing(prompt, expected)
    # prompt = f'db-ls --catalog bluesky-tutorial-BMM --number 2 --reverse'
    # expected = """Loading the 'bluesky-tutorial-BMM' Catalog...\n     Starting Time          Scan ID      UUID\n      2021-06-24 18:41:37     42085     c5b4ca9b\n      2021-06-24 18:48:22     64366     9e36935f"""
    # arg_testing(prompt, expected)


def test_tail():
    prompt = f'db-ls --tail --catalog bluesky-tutorial-RSOXS'
    expected = """Loading the 'bluesky-tutorial-RSOXS' Catalog...\n     Starting Time          Scan ID      UUID\n      2019-11-17 04:28:56     6959     777b44ae"""
    arg_testing(prompt, expected)
    prompt = f'db-ls --tail --catalog bluesky-tutorial-BMM --number 2'
    expected = """Loading the 'bluesky-tutorial-BMM' Catalog...\n     Starting Time          Scan ID      UUID\n      2020-03-03 04:33:05     22524     51f9eb19\n      2020-03-03 04:18:06     22521     f8c83910"""
    arg_testing(prompt, expected)
    prompt = f'db-ls --tail --catalog bluesky-tutorial-BMM --number -2'
    arg_testing(prompt, expected)
    prompt = f'db-ls --catalog bluesky-tutorial-BMM --number -2'
    arg_testing(prompt, expected)
    # prompt = f'db-ls --catalog bluesky-tutorial-BMM --number -2 --reverse'
    # expected = """Loading the 'bluesky-tutorial-BMM' Catalog...\n     Starting Time          Scan ID      UUID\n      2020-03-03 04:18:06     22521     f8c83910\n      2020-03-03 04:33:05     22524     51f9eb19"""
    # arg_testing(prompt, expected)


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

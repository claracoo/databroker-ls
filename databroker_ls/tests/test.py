#!/usr/bin/env python3
"""tests for hello.py"""

import os
from subprocess import getstatusoutput, getoutput

import msgpack
import numpy as np
import pytest

from bluesky import RunEngine
from bluesky.plans import count
from event_model import sanitize_doc
from ophyd.sim import det


prg = '/Users/claracook/Desktop/test/databroker-ls/databroker_ls/stupid-ls.py'


# --------------------------------------------------
def test_exists():
    """exists"""

    assert os.path.isfile(prg)


# --------------------------------------------------
def test_runnable():
    """Runs using python3"""

    out = getoutput(f'python3 {prg}')
    assert out.strip() != 'Hello, World!'


# --------------------------------------------------
def place_data():
    RE = RunEngine()
    RE.subscribe(bluesky_publisher)
    RE.subscribe(store_published_document)

    RE([count(det)])




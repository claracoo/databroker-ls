import databroker.tutorial_utils

databroker.tutorial_utils.fetch_RSOXS_example()

import databroker

from bluesky import RunEngine
from ophyd.sim import det, motor, SynSignal, det4, motor1, motor2
from bluesky.plans import count, scan, grid_scan

from bluesky_widgets.utils.streaming import stream_documents_into_runs
from bluesky_widgets.models.plot_builders import Lines
from bluesky_widgets.qt.figures import QtFigure

import tempfile
from suitcase.msgpack import Serializer
import numpy as np

from databroker._drivers.msgpack import BlueskyMsgpackCatalog

databroker.tutorial_utils.fetch_BMM_example()
catalog = databroker.catalog['bluesky-tutorial-BMM']

import pandas as pd
from datetime import datetime

def toReadableDate(linuxtime):
  return datetime.utcfromtimestamp(linuxtime).strftime('%Y-%m-%d %H:%M:%S')

def ls():
  data = [[toReadableDate(catalog[x].metadata["start"]["time"]), catalog[x].metadata["start"]["scan_id"], catalog[x].metadata["start"]["uid"],] for x in catalog]

  indexing = pd.Series([x for x in range(-1, (len(catalog) + 1) * -1, -1)])

  df = pd.DataFrame(data, columns =['Start Time', 'Scan ID', 'UUID']).set_index(indexing)
  df.index.name = 'Backwards Index'
  return df

print(ls())
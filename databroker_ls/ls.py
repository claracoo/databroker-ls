#!/usr/bin/env python3

from databroker import catalog
from databroker.queries import TimeRange
import pandas as pd
from datetime import datetime

import databroker.tutorial_utils

from bluesky import RunEngine
from ophyd.sim import det, motor, SynSignal, det4, motor1, motor2
from bluesky.plans import count, scan, grid_scan

from bluesky_widgets.utils.streaming import stream_documents_into_runs
from bluesky_widgets.models.plot_builders import Lines

# from bluesky_widgets.qt.figures import QtFigure

from databroker_ls.args import get_args

import tempfile
from suitcase.msgpack import Serializer
import tableprint as tp
import numpy as np

from datetime import datetime
import argparse

from databroker._drivers.msgpack import BlueskyMsgpackCatalog


class ls:
    """
    This class gets the data that we are going to list out.
    """

    uuids = []  # list of the uuids as strings, will be ordered newest to oldest
    catalog = catalog  # the literal catalog we pass it
    fullID = False  # whether or not we want the whole UUID or just the first 8 chars, see self.uuidLen
    reverse = False  # if true, data will be listed oldest to newest
    UUIDtoIndex = {}  # the uuid (the 8 char long version) to thebackwards index
    uuidLen = 8  # standard for uuid length
    number = 0  # if it is 0, we will ignore it, if it is negative, we want the tail, if its posiitve we want the head

    def __init__(self, catalog, fullUID, reverse, number):
        super().__init__()
        self.catalog = catalog
        for i in range(len(list(catalog))):  # setup for the uuids and the UUIDtoIndex
            index = -1 * (i + 1)  # how we get the backwards index
            uuid = (
                catalog[index].metadata["start"].get("uid", "")[: self.uuidLen]
            )  # the uuid condensed down to our desired length
            self.uuids.append(uuid)
            self.UUIDtoIndex[uuid] = index
        if fullUID:  # we get the whole UUID
            self.uuidLen = 36
        self.reverse = reverse
        self.number = number
        if number < 0 and abs(number) >= len(
            list(catalog)
        ):  #  if the catalog is shorter than the number the user requested, we just show the whole catalog
            self.number = 0

    def to_readable_date(self, linuxtime):
        """Linux time to human readable date and time"""
        return datetime.utcfromtimestamp(linuxtime).strftime("%Y-%m-%d %H:%M:%S")

    def organize_data(self):
        """
        This function takes the uuids loaded in the init function and picks out what we want to list
        """
        howManyEntries = len(list(self.catalog))  # assume we want every entry
        if (
            self.number != 0
        ):  # if the user specifies that they don't want every entry, we update how many we will see
            howManyEntries = abs(self.number)
        data = []
        i = 0
        for index in self.UUIDtoIndex.values():  # assume we are going thru all runs
            if i < howManyEntries:  # limit it to how many entries the user wants to see
                counter = index  # normal
                if self.number < 0:
                    counter = howManyEntries - (
                        len(list(self.catalog)) + abs(index)
                    )  # reverse
                data.append(
                    [
                        self.to_readable_date(
                            self.catalog[counter]
                            .metadata["start"]
                            .get("time", "None               ")
                        ),  # make the data something a human could understand
                        self.catalog[counter].metadata["start"].get("scan_id", "None "),
                        (
                            self.catalog[counter]
                            .metadata["start"]
                            .get("uid", "None    ")
                        )[: self.uuidLen],
                    ]
                )
            i += 1
        return data

    def output_data(self):
        data = self.organize_data()  # assume not reversed
        if self.reverse:
            data = data[::-1]  # reverse it
        return data

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
    """This class holds the act of going from the searching the catalog to a pandas dataframe"""

    catalog = []  # particular catalog we're referencing
    fullUID = False
    removableCatalog = (
        []
    )  # the catalog's list of UUIDs will be copied in here, and then removed as they are printed
    TIME = ""  # this is a parameter I may want to change later
    CHUNK_SIZE = 10  # how many entries get loaded in each group
    UUIDtoIndex = {}
    reverse = False
    number = 100

    def __init__(self, catalog, fullUID, reverse, number):
        """
        The goal is to load all UUIDs into the removableCatalog variable
        This way, the user can load as many or as few entries as they choose
        PROBLEM: These are unordered
        """

        super().__init__()
        self.catalog = catalog
        self.fullUID = fullUID
        self.reverse = reverse
        self.CHUNK_SIZE = number
        query = TimeRange()  # when no time range is specified, it loads all entries
        self.removableCatalog = list(
            self.catalog.search(query)
        )  # how all the UUIDs are loaded into removable catalog
        UUIDtoTime = {
            self.removableCatalog[x]: self.catalog[self.removableCatalog[x]].metadata[
                "start"
            ]["time"]
            for x in range(len(self.removableCatalog))
        }
        if self.reverse:
            self.removableCatalog = list(
                x[0] for x in sorted(UUIDtoTime.items(), key=lambda x: x[1])
            )
            self.UUIDtoIndex = {self.removableCatalog[k][:8]: (-1) * (len(self.removableCatalog) - k) for k in
                                range(len(self.removableCatalog))}
        else:
            self.removableCatalog = list(
                x[0] for x in sorted(UUIDtoTime.items(), key=lambda x: x[1], reverse=True)
            )
            self.UUIDtoIndex = {self.removableCatalog[k][:8]: ((-1) * k) - 1 for k in
                                range(len(self.removableCatalog))}


    def getCurrentSubcatalog(self, chunk_size):
        """ "
        Helper function for toPandas() method
        This gets the next section of the catalog to display
        Removes the UUIDS used from removableCatalog
        """

        currentView = self.removableCatalog[
            :chunk_size
        ]  # puts the UUIDs we are looking at in a smaller list
        del self.removableCatalog[
            :chunk_size
        ]  # removes same UUIDs from removableCatalog
        return currentView

    def toReadableDate(self, linuxtime):
        """Linux time to human readable date and time"""
        return datetime.utcfromtimestamp(linuxtime).strftime("%Y-%m-%d %H:%M:%S")


    def myOwnPrinting(self):
        """ "Formats the array necessary to print things later"""
        currentView = self.getCurrentSubcatalog(
            self.CHUNK_SIZE
        )  # get what we want to load so far
        uuidLen = 8  # standard option is to only show half the uid
        if self.fullUID:
            uuidLen = 36
            # if the user specifies that they want the whole thing, it is 36 chars long
        data = [
            [
                self.toReadableDate(
                    self.catalog[x].metadata["start"].get("time", "None               ")
                ),  # make the data something a human could understand
                self.catalog[x].metadata["start"].get("scan_id", "None "),
                (self.catalog[x].metadata["start"].get("uid", "None    "))[:uuidLen],
            ]
            for x in currentView
        ]  # gets the time, scan_id and beginning of uid
        if len(data) != 0:
            return (
                data,
                "Hit enter to see more or press esc to exit",
            )  # includes array from which we want to print, and helpful message
        else:
            return (
                data,
                "exit",
            )  # data should be empty --> allows the return type at 0 and 1 to always exist
            # the word exit is a shorthand key term that is checked in the file command_line.py


# --------------------------------------------------
def main():
    """Make a jazz noise here"""
    # object = ls(catalog["bluesky-tutorial-BMM"])  # instantiates object


# --------------------------------------------------
if __name__ == "__main__":
    main()

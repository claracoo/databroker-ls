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

    def __init__(self, catalog, fullUID):
        """
        The goal is to load all UUIDs into the removableCatalog variable
        This way, the user can load as many or as few entries as they choose
        PROBLEM: These are unordered
        """

        super().__init__()
        self.catalog = catalog
        self.fullUID = fullUID
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
        self.removableCatalog = list(
            x[0] for x in sorted(UUIDtoTime.items(), key=lambda x: x[1], reverse=True)
        )
        self.UUIDtoIndex = {self.removableCatalog[k][:8]: ((-1) * k) - 1 for k in
                   range(len(self.removableCatalog))}
        self.CHUNK_SIZE = get_args().number

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

    def toPandas(self):
        """
        Takes the UUIDs and puts them into actual bluesky runs
        Takes these runs to get info that we can list for users, to make runs easier to find
        """

        # currentView = self.getCurrentSubcatalog(self.CHUNK_SIZE) # get what we want to load so far
        # #next line: actual information we want to format (get info from bluesky runs)
        # data = [[self.toReadableDate(self.catalog[x].metadata["start"]["time"]), self.catalog[x].metadata["start"]["scan_id"], (self.catalog[x].metadata["start"]["uid"])[:8]] for x in currentView]
        #
        # indexing = pd.Series([x for x in range(-1, (len(currentView) + 1) * -1, -1)]) # default pandas indexing is misleading --> turn into something databroker actuall uses (backward index)
        #
        # df = pd.DataFrame(data, columns =['Start Time', 'Scan ID', 'UUID Partial']).set_index(indexing) # label the columns and set the indexes to indexing made in prev line
        # df.index.name = 'Backwards Index' # give index column a name
        return self.myOwnPrinting()
        # return df

    def toTablePrint(self):
        """This was an ugly printing idea"""
        currentView = self.getCurrentSubcatalog(
            self.CHUNK_SIZE
        )  # get what we want to load so far
        # next line: actual information we want to format (get info from bluesky runs)
        # data = np.array(
        #     [
        #         [
        #             self.toReadableDate(self.catalog[x].metadata["start"]["time"]),
        #             self.catalog[x].metadata["start"]["scan_id"],
        #             (self.catalog[x].metadata["start"]["uid"])[:8],
        #         ]
        #         for x in currentView
        #     ]
        # )
        # tp.banner("Welcome to tableprint!")
        # tp.table(data, ["Start Time", "Scan ID", "Partial UUID"])

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

    # def get_backwards_index(self):
    #     return UUIDtoIndex



# --------------------------------------------------
def main():
    """Make a jazz noise here"""
    # object = ls(catalog["bluesky-tutorial-BMM"])  # instantiates object


# --------------------------------------------------
if __name__ == "__main__":
    main()

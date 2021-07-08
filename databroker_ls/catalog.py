import sys
from databroker import catalog

import yaml


class SpecifiedCatalog:
    currentCatalog = ""

    def __init__(self):
        """
        The only goal of this class is to set up the catalog.
        """

        super().__init__()
        self.currentCatalog = ""  # acts as a buffer between the catalog used in the

    def query_for_catalog(self, default):
        """
        Explain to the user how to set their default choice.
        This will only be called once,
        the first time they install this package.
        """

        valid = list(
            catalog
        )  # we want to only use the catalogs that exist in the given catalogs
        if default in valid:  # check that the default option is a valid choice
            prompt = f"You do not have a default catalog selected.\nPlease select a catalog to reference. The current available catalogs are:\n {valid}\nCatalog Choice: "  # what the user will see in terminal
        else:  # if the default is not valid, something has gone wrong
            raise ValueError("invalid default answer: '%s'" % default)
        while True:  # until the user makes an action, we should be stuck at this prompt
            sys.stdout.write(prompt)  # send user the situation
            choice = (
                input().replace('"', "").replace("'", "").replace(" ", "").strip()
            )  # normalize their input
            if (
                choice == ""
            ):  # if they hit enter and put no input, give them the default
                sys.stdout.write(
                    f"\nYou have chosen the default, or the {default} catalog.\n\nLoading catalog...\n"
                )  # what the user sees when they choose default
                self.currentCatalog = (
                    default  # set our buffer variable to reflect their choice
                )
                return False  # get out of prompt
            elif choice in valid:  # make sure their input is a valid catalog
                sys.stdout.write(
                    f"\nYou have chosen the {choice} catalog.\n\nLoading catalog...\n"
                )  # what the user sees
                self.currentCatalog = (
                    choice  # set our buffer variable to reflect their choice
                )
                return False  # get out of prompt
            else:  # if their choice is not valid
                sys.stdout.write(
                    f"\nYou responded with {choice}.\nThis is not one of the available catalogs.\n\n"
                )  # tell user to try again

    def change_default_catalog(self, filename, new_catalog):
        """
        This function puts the key value pair in the yml file.
        This should be of the form:
            'catalog_name': [SOME CATALOG]
        """

        data = {"catalog_name": new_catalog}  # set up the key value pair
        with open(filename, "w+") as f:  # open file to write there
            yaml.dump(data, f)  # put the key value pair in the yml file

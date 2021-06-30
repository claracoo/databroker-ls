import sys
from databroker import catalog

class SpecifiedCatalog:
    currentCatalog = ""

    def __init__(self):
        """
        The goal is to load all UUIDs into the removableCatalog variable
        This way, the user can load as many or as few entries as they choose
        PROBLEM: These are unordered
        """

        super().__init__()
        self.currentCatalog = ""


    def query_for_catalog(self, default="bluesky-tutorial-BMM"):
        valid = list(catalog)
        if default in valid:
            prompt = f"Please select a catalog to reference. The current available catalogs are:\n {valid}\nCatalog Choice: "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(prompt)
            choice = input().strip("'")
            choice = choice.strip('"')
            if choice == "":
                sys.stdout.write(f"\nYou have chosen the default, or the {default}, catalog.\n\nLoading catalog...\n")
                self.currentCatalog = default
                return False
            elif choice in valid:
                sys.stdout.write(f"\nYou have chosen the {choice} catalog.\n\nLoading catalog...\n")
                self.currentCatalog = choice
                return False
            else:
                sys.stdout.write(f"\nYou responded with {choice}.\nThis is not one of the available catalogs.\n\n")

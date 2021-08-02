from databroker_ls.command_line import get_current_catalog
from databroker import catalog

import databroker_ls
from os import path

path_prefix = path.split(databroker_ls.__path__[0])[0]
file = path.join(path_prefix, "conf_catalog.yml")


def main():
    currentCatalog = get_current_catalog(file)
    print("hi")
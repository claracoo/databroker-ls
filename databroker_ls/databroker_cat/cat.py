from databroker_ls.command_line import get_current_catalog
from databroker import catalog

file = "../conf_catalog.yml"

def main():
    currentCatalog = get_current_catalog(file)

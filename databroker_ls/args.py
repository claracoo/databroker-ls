import argparse
from databroker_ls.catalog import SpecifiedCatalog

def get_args():
    specifiedCatalog = SpecifiedCatalog()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--catalog',
        help='Pass the catalog you want to list',
        type=str,
        dest='catalog',
        default=specifiedCatalog.currentCatalog
    )
    parser.add_argument(
        '-n',
        '--number',
        help='How many data points do you want to be shown in one load',
        type=int,
        dest='number',
        default=10
    )
    parser.add_argument(
        '-a',
        '--all',
        action='store_true',
        dest='all',
        help='Show full UID'
    )
    parser.add_argument(
        '-i',
        '--index',
        action='store_true',
        dest='index',
        help='Show backwards indices'
    )
    parser.add_argument(
        '-r',
        '--reverse',
        action='store_true',
        dest='reverse',
        help='List the runs in reverse order (oldest to newest)'
    )
    args = parser.parse_args()
    return args

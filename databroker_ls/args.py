import argparse
parser = argparse.ArgumentParser()
parser.add_argument(
    '-c',
    '--catalog',
    help='Pass the catalog you want to list',
    type=str,
    dest='catalog',
    default='bluesky-tutorial-BMM'
)
args = parser.parse_args()
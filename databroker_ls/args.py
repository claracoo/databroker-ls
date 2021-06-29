import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--catalog',
        help='Pass the catalog you want to list',
        type=str,
        dest='catalog',
        default='bluesky-tutorial-BMM'
    )
    parser.add_argument(
        '-a',
        '--all',
        action='store_true',
        help='Show full UID'
    )
    args = parser.parse_args()
    return args

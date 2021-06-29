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
        '-n',
        '--number',
        help='Pass the catalog you want to list',
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
    args = parser.parse_args()
    return args

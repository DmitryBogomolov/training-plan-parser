import sys
from argparse import ArgumentParser
from .processor import process, process_file

def run(*args):
    parser = ArgumentParser(description='Parses and renders training plan.')
    parser.add_argument('source', type=str, nargs='?', help='path to plan')
    args = parser.parse_args(*args)
    if args.source == '-':
        process(sys.stdin.buffer, sys.stdout.buffer)    # pylint: disable=no-member
    elif args.source:
        process_file(args.source)
    else:
        parser.print_help()

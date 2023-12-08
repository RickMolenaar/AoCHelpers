import argparse
import datetime
from datetime import datetime
import importlib
import os
import time

from AoCHelpers import generator, AoCWatcher
from AoCHelpers.functions import day_of_month

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--day', help="Which day to run")
    parser.add_argument('-g', '--generate', action='store_true',  help="Whether todays files should be generated")
    parser.add_argument('-t', '--time', action='store_true')
    parser.add_argument('-r', '--run', action='store_true')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--countdown', '--cd', action='store_true')
    return parser.parse_args()

def run(year = None):
    args = parse_arguments()
    if year is None:
        year = datetime.datetime.today().year
    if args.day is None:
        day = day_of_month()
    else:
        day = int(args.day)
    
    if not args.generate and not os.path.exists(f"day{day:0>2}.py"):
        raise ValueError(f"Generator parameter was not supplied and file doesn't exist: day{day:0>2}.py")
    if args.generate:
        generator.generate(day, year, args.countdown)
    elif args.time:
        module = importlib.import_module(f"day{day:0>2}")
        t0 = time.time()
        for res in module.main():
            print(res)
        print(f'Done in {time.time() - t0} s')
    else:
        args.run = True
    if args.run:
        watcher = AoCWatcher.Watcher(year, day)
        watcher.watch()
import argparse
from importlib import import_module, reload
import os
import time
import traceback

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('module')
    parser.add_argument('function')
    parser.add_argument('-v', '--verbose', action='store_true')
    
    args = parser.parse_args()
    if not args.module.endswith('.py'):
        args.module = args.module + '.py'
    if not os.path.exists(args.module):
        raise ValueError(f"Invalid module: {args.module}")
    
    return args


class Watcher:
    def __init__(self, filename, function, *additional_files, interval = 1, verbose = False, **additional_args):
        self.filename = filename
        self.to_watch = (filename,) + additional_files
        self.function = function
        self.last_modified_times = [0] * len(self.to_watch)
        self.interval = 1
        self.verbose = verbose
        self.additional_args = additional_args
        self.previously_found = False
        try:
            self.module = import_module(filename[:-3])
        except (SyntaxError, IndentationError, NameError):
            self.module = None    # Will be caught in run()

    def watch(self):
        print(f"Watching function {self.function}, files: {self.to_watch}")
        try:
            while True:
                modified = False
                for i, filename in enumerate(self.to_watch):
                    modified_time = os.stat(filename).st_mtime
                    if modified_time > self.last_modified_times[i]:
                        modified = True
                        if self.verbose:
                            print(f"File {filename} was changed")
                        self.last_modified_times[i] = modified_time
                if modified:
                    self.run()
                time.sleep(self.interval)

        except KeyboardInterrupt:
            print('Stopping watcher')
            return

    def run(self):
        try:
            if self.module is None:
                self.module = import_module(self.filename[:-3])
            module = reload(self.module)
        except (SyntaxError, IndentationError) as e:
            print('Could not load module')
            print(traceback.format_exc())
            return
        try:
            func = getattr(module, self.function)
        except AttributeError:
            if not self.previously_found:
                print(f"No function {self.function} found in module {self.filename}.py")
            self.previously_found = False
            return
        self.previously_found = True
        try:
            result = func(**self.additional_args)
        except KeyboardInterrupt:
            raise
        except Exception:
            print('Watched method failed with error:')
            print(traceback.format_exc())
        else:
            if self.verbose:
                print('Watched method returned: ', end = '')
            print(result)
        print('-' * 5)

if __name__=='__main__':
    args = parse_arguments()
    watcher = Watcher(args.module, args.function, verbose = args.verbose)
    watcher.watch()
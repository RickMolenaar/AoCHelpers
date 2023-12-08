import traceback
from typing import Any
from pathlib import Path

from AoCHelpers import pywatch
from AoCHelpers.communicator import Communicator


CWD = str(Path.cwd())

class Watcher(pywatch.Watcher):
    def __init__(self,
                 year: int,
                 day: int,
                 *additional_files: str,
                 interval: int = 1, 
                 verbose: bool = False, 
                 **additional_args: Any):
        filename = f'day{day:0>2}.py'
        additional_files = (f'day{day:0>2}example.txt', f'day{day:0>2}.txt')
        super().__init__(filename, 'main', *additional_files, interval = interval, verbose = verbose, **additional_args)
        self.answers = []
        self.year = year
        self.day = day
        self.communicator = Communicator()
        self.read_stats()
        
    def handle_interrupt(self, during_run: bool) -> None:
        if during_run:
            print('Interrupting run, press enter to rerun')
            input()
        else:
            part = self.stats[self.day - 1] + 1
            print('What would you like to do?')
            if part in (1, 2):
                print(f'[S]ubmit answer for part {part}')
            print('[Q]uit watcher')
            print('[C]ontinue')
            inp = input()
            valid = False
            inp = inp.lower()
            while not valid:
                inp = inp.lower()
                if not inp or inp not in 'sqc':
                    inp = input('Unrecognized command\n')
                elif inp == 's' and part > 2:
                    inp = input('All parts have been submitted\n')
                else:
                    valid = True
            if inp == 's':
                result = self.communicator.submit_answer(self.year, self.day, part, self.answers[-1])
                if result:
                    self.stats[self.day - 1] += 1
                    self.write_stats()
                print('-' * 5)
                return False
            elif inp == 'q':
                return True
            else:
                print('-' * 5)
                return False

    def handle_output(self, result):
        for part in (1, 2):
            if part == 2 and self.stats[self.day - 1] == 0:
                continue
            for example in (True, False):
                try:
                    res = next(result)
                except KeyboardInterrupt:
                    self.handle_interrupt(True)
                    return
                else:
                    if isinstance(res, Exception):
                        print(f'Error during part {part} {"example" if example else "actual"}:')
                        traceback.print_exception(res)
                    else:
                        print(f'Part {part} {"example" if example else "actual "}: {res}')
                        if not example and res is not None:
                            self.answers.append(res)

    def read_stats(self):
        try:
            stats_file = open(CWD + '/stats.txt')
            self.stats = []
            for line in stats_file:
                self.stats.append(int(line))
        except FileNotFoundError:
            self.stats = [0] * 25
            self.write_stats()

    def write_stats(self):
        f = open(CWD + '/stats.txt', 'w')
        for i in range(25):
            f.write(str(self.stats[i]) + '\n')

if __name__=='__main__':
    pass
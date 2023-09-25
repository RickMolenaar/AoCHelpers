import traceback
from typing import Any, Callable
from pathlib import Path

from . import pywatch
from .communicator import Communicator


CWD = Path.cwd()

class Watcher(pywatch.Watcher):
    def __init__(self,
                 year: int,
                 day: int,
                 *additional_files: str,
                 interval: int = 1, 
                 verbose: bool = False, 
                 **additional_args: Any):
        filename = f'day{day}.py'
        additional_files = (f'day{day}example.txt', f'day{day}.txt')
        super().__init__(filename, 'main', *additional_files, interval = interval, verbose = verbose, **additional_args)
        self.answers = []
        self.verified_answers = []
        self.year = year
        self.day = day
        self.communicator = Communicator()
        
    def handle_interrupt(self, during_run: bool) -> None:
        if during_run:
            print('Interrupting run, press enter to rerun')
            input()
        else:
            print('What would you like to do?')
            print(f'[S]ubmit answer for part {len(self.verified_answers) + 1}')
            print('[Q]uit watcher')
            print('[C]ontinue')
            inp = input()
            while inp.lower() not in 'sqc':
                inp = input('Unrecognized command\n')
            inp = inp.lower()
            if inp == 's':
                self.communicator.submit_answer(self.year, self.day, self.answers[-1])
            elif inp == 'q':
                return True
            else:
                print('-' * 5)
                return False

    def handle_output(self, result):
        for part in (1, 2):
            for example in (True, False):
                try:
                    res = next(result)
                except KeyboardInterrupt as e:
                    self.handle_interrupt(True)
                except Exception:
                    print(f'Error during part {part} {"example" if example else "actual"}:')
                    print(traceback.format_exc())
                else:
                    print(f'Part {part} {"example" if example else "actual "}: {res}')
                    if not example:
                        self.answers.append(res)

if __name__=='__main__':
    pass
import datetime
import os
from time import sleep

from bs4 import BeautifulSoup, Tag

from .communicator import Communicator
from .tools import day_of_month, EST_now, EST


TEMPLATE_FILE = """def parse_input(file = 'day{day:0>2}.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day{day:0>2}example.txt')

def format_input(inp: list[str]):
    return inp

def solve(inp, part, example):
    return None

def main():
    example_input = format_input(parse_example())
    actual_input = format_input(parse_input())
    for part in (1, 2):
        for example in (True, False):
            inp = example_input if example else actual_input
            try:
                yield solve(inp, part, example)
            except KeyboardInterrupt:
                raise
            except Exception as e:
                yield e
"""

def generate(day: int, year: int, countdown: bool) -> None:
    communicator = Communicator()
    if os.path.exists(f"day{day:0>2}.py"):
        print(f'day{day:0>2}.py already exists. Continue generating? (y/n)')
        inp = input()
        while inp.lower() not in 'yn':
            inp = input('(y/n) ')
        if inp.lower() == 'n':
            return
        
    with open(f"day{day:0>2}.py", "w") as f:
        f.write(TEMPLATE_FILE.format(day = day))
        
    if day > day_of_month() and year >= datetime.date.today().year and not countdown:
        open(f"day{day:0>2}.txt", "w").close()
        open(f"day{day:0>2}example.txt", "w").close()
        return
    elif countdown:
        target = datetime.datetime(year, 12, day, second=2, tzinfo=EST())   # Avoid time sync issues
        to_wait = (target - EST_now()).seconds
        print(f'Counting down {to_wait} seconds')
        try:
            if to_wait > 60:
                sleep(to_wait - 60)
                print('One minute left')
                to_wait = (target - EST_now()).seconds  #Ensure accuracy
            if to_wait > 10:
                sleep(to_wait - 10)
                print('10 seconds left')
                to_wait = (target - EST_now()).seconds
            if to_wait > 1:
                sleep(to_wait - 1)
            while EST_now() < target:
                sleep(0.1)
        except KeyboardInterrupt:
            print('Countdown interrupted, writing empty files')
            open(f"day{day:0>2}.txt", "w").close()
            open(f"day{day:0>2}example.txt", "w").close()
            return

    with open(f"day{day:0>2}.txt", "w") as f:
        f.write(communicator.get_input(year, day))

    problem_page = communicator.get_problem(year, day)
    problem_page = BeautifulSoup(problem_page, features='html.parser')
    part1 = problem_page.find(name='article')
    if part1 is None:
        print("Could not parse page")
        open(f"day{day:0>2}example.txt", "w").close()
        return
    example_candidates = find_example(part1)
    if len(example_candidates) == 1:
        example = example_candidates[0][1]
        print('Writing example to file:')
        print(example.text)
        with open(f"day{day:0>2}example.txt", "w") as f:
            f.write(example.text)
    else:
        for candidate in example_candidates:
            print('Potential example:')
            print(candidate[0].text)
            print(candidate[1].text)
            print('=' * 30)
        open(f"day{day:0>2}example.txt", "w").close()

def find_example(article: Tag) -> list[tuple[str, str]]:
    children = [c for c in list(article.children) if c != '\n']
    candidates = find_example_candidates(children)
    if not candidates:
        candidates = find_example_candidates(children, strict=False)
        if not candidates:
            print('Could not find an example')
    if len(candidates) > 1:
        print('Multiple possible examples found')
    return candidates

def find_example_candidates(elements, strict = True):
    candidates = []
    to_find = 'for example' if strict else 'example'
    for i, el in enumerate(elements):
        if i == len(elements) - 1:
            continue
        if elements[i+1].name == 'pre':
            if to_find in el.text.lower():
                candidates.append((el, elements[i+1]))
    return candidates

def find_example_result(article: Tag) -> list[str]:
    code_elements = article.find_all(name='code')
    return [el for el in code_elements if el.find(name='em')]

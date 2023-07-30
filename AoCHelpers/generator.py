import datetime
import requests

from bs4 import BeautifulSoup, Tag
from pathlib import Path

CWD = Path.cwd()

TEMPLATE_FILE = """def parse_input(file = 'day{day:0>2}.txt'):
    with open(file) as f:
        s = map(lambda l: l.rstrip(), f.readlines())
    return list(s)

def parse_example():
    return parse_input('day{day:0>2}example.txt')

def format_input(inp):
    return inp

def solve(inp, debug=False):
    inp = format_input(inp)
    return None

def main(debug = False):
    return str(solve(parse_example(), True)) + '\\n' + str(solve(parse_input(), debug))
"""

def generate(day: int, year: int) -> None:
    with open(f"{CWD}/day{day:0>2}.py", "w") as f:
        f.write(TEMPLATE_FILE.format(day = day))
        
    if day <= datetime.datetime.today().day:
        input_page = get_page(f"/{year}/day/{day}/input")
        if input_page.status_code != 200:
            print(input_page.status_code, input_page.reason)
            open(f"{CWD}/day{day:0>2}.txt", "w").close()
        else:
            with open(f"{CWD}/day{day:0>2}.txt", "w") as f:
                f.write(input_page.text)

        problem_page = get_page(f"/{year}/day/{day}")
        if problem_page.status_code != 200:
            print(problem_page.status_code, problem_page.reason)
            open(f"{CWD}/day{day:0>2}.txt", "w").close()
            open(f"{CWD}/day{day:0>2}example.txt", "w").close()
        else:
            problem_page = BeautifulSoup(problem_page.content, features='html.parser')
            part1 = problem_page.find(name='article')
            example_candidates = find_example(part1)
            if len(example_candidates) == 1:
                example = example_candidates[0][1]
                print('Writing example to file:')
                print(example.text)
                with open(f"{CWD}/day{day:0>2}example.txt", "w") as f:
                    f.write(example.text)
            else:
                for candidate in example_candidates:
                    print('Potential example:')
                    print(candidate[0].text)
                    print(candidate[1].text)
                    print('=' * 30)
                open(f"{CWD}/day{day:0>2}example.txt", "w").close()
    else:
        open(f"{CWD}/day{day:0>2}.txt", "w").close()
        open(f"{CWD}/day{day:0>2}example.txt", "w").close()


def get_page(location: str) -> requests.Response:
    with open('session.cookie') as f:
        cookie = f.readline()
    if not location.startswith('/'):
        location = '/' + location
    return requests.get(f'https://adventofcode.com' + location, cookies={'session': cookie})

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

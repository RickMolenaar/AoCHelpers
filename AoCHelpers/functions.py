from datetime import datetime, timedelta, tzinfo
from typing import Literal

class EST(tzinfo):
    def utcoffset(self, __dt: datetime | None) -> timedelta:
        return timedelta(hours=-5)
    
    def dst(self, dt):
        return timedelta(0)
    
    def tzname(self,dt):
        return "EST"

    def  __repr__(self):
        return f"{self.__class__.__name__}()"

def day_of_month() -> int:
    return datetime.now(tz = EST()).day

def EST_now() -> datetime:
    return datetime.now(tz = EST())

def lcm(a, b):
    return a // gcd(a, b) * b

def gcd(a, b):
    while b != 0:
        t = b
        b = a % b
        a = t
    return a

def rotate(to_rotate: tuple[int, int], about: tuple[int, int], direction: Literal['cw', 'ccw'], ypos: Literal['up', 'down'] = 'up'):
    if direction not in ('cw', 'ccw'):
        raise ValueError('direction must be either \'cw\' or \'ccw\'')
    if ypos not in ('up', 'down'):
        raise ValueError('ypos must be either up or down')
    x, y = to_rotate
    ox, oy = about
    dx, dy = x - ox, y - oy
    match direction, ypos:
        case ('cw', 'up') | ('ccw', 'down'):
            dx, dy = dy, -dx
        case ('ccw', 'up') | ('cw', 'down'):
            dx, dy = -dy, dx
        case _:
            raise ValueError
    return ox + dx, oy + dy
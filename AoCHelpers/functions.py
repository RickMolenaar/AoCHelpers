from datetime import datetime, timedelta, tzinfo

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
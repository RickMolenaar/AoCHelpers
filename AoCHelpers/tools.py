from datetime import datetime, timedelta, tzinfo

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
def generate_primes(max):
    ls = [True for _ in range(max + 1)]
    for m in range(max // 2 + 1):
        ls[2 * m] = False
    ls[1] = False
    primes = [2]
    p = 3
    while p < len(ls):
        if ls[p]:
            for m in range(p, max // p + 1, 2):
                ls[p * m] = False
            primes.append(p)
        p += 2
    return primes

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
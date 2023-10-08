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

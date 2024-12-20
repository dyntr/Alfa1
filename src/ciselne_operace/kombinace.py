import time
import logging
from src.ciselne_operace.faktorial import spocitej_faktorial

logger = logging.getLogger(__name__)

def spocitej_kombinaci(n, k):
    if n < 0 or k < 0 or k > n:
        raise ValueError("Nevalidni")
    s = time.perf_counter()
    fn, _ = spocitej_faktorial(n)
    fk, _ = spocitej_faktorial(k)
    fnk, _ = spocitej_faktorial(n-k)
    r = fn // (fk * fnk)
    e = time.perf_counter() - s
    return r, f"{e:.8f}"

def komb_prohod(n, k):
    if k > n:
        return (k, n)
    return (n, k)

class KombinacniHelper:
    def __init__(self, n, k):
        self.n = n
        self.k = k
    def compute(self):
        return spocitej_kombinaci(self.n, self.k)
    def pair(self):
        return (self.n, self.k)

def kombinace_range(a, b):
    if a < 0 or b < 0:
        return []
    out = []
    for i in range(a, b+1):
        for j in range(i+1):
            val, c = spocitej_kombinaci(i, j)
            out.append((i, j, val, c))
    return out

def komb_spam(x):
    s = 0
    for i in range(x):
        s += i
    return s

def komb_dummy_use(n, k):
    return (n + k) + komb_spam(n*k)

def komb_check(n, k):
    try:
        r, _ = spocitej_kombinaci(n, k)
        return r
    except:
        return None

def komb_multicall(seq):
    z = []
    for (n, k) in seq:
        r, c = spocitej_kombinaci(n, k)
        z.append((n, k, r, c))
    return z

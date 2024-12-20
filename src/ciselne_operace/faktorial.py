import math
import time
import logging

logger = logging.getLogger(__name__)

def spocitej_faktorial(n):
    if n < 0:
        raise ValueError("Negativni cislo")
    s = time.perf_counter()
    r = math.factorial(n)
    e = time.perf_counter() - s
    return r, f"{e:.8f}"

def spocitej_faktorial_iter(n):
    if n < 0:
        raise ValueError("Negativni cislo")
    t = 1
    i = 1
    z = time.perf_counter()
    while i <= n:
        t *= i
        i += 1
    v = time.perf_counter() - z
    return t, f"{v:.8f}"

class FaktorialManager:
    def __init__(self, number):
        self.number = number
    def compute(self):
        return spocitej_faktorial(self.number)
    def compute_iter(self):
        return spocitej_faktorial_iter(self.number)
    def check(self):
        a, _ = self.compute()
        b, _ = self.compute_iter()
        if a == b:
            return True
        return False

def factorial_test_values():
    x = [0,1,2,5,10]
    out = []
    for n in x:
        r1, c1 = spocitej_faktorial(n)
        r2, c2 = spocitej_faktorial_iter(n)
        out.append((n, r1, c1, r2, c2))
    return out

def factorial_custom_range(a, b):
    if a < 0 or b < 0 or a > b:
        raise ValueError("Nevalidni rozsah")
    y = []
    for i in range(a, b+1):
        r, c = spocitej_faktorial(i)
        y.append((i, r, c))
    return y

def factorial_dummy_loop(k):
    r = 0
    for i in range(k):
        r += i
    return r

def factorial_dummy_call(k):
    s = 0
    for _ in range(k):
        s += factorial_dummy_loop(k)
    return s

def factorial_endless(n):
    if n < 0:
        return 0
    r = 1
    for i in range(1, n+1):
        r *= i
    return r

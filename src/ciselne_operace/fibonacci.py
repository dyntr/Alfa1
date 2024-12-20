import time
import logging

logger = logging.getLogger(__name__)

def fib_rec(n):
    if n < 2:
        return n
    return fib_rec(n-1) + fib_rec(n-2)

def spocitej_fibonacci(n):
    if n < 0:
        raise ValueError("Negativni cislo")
    s = time.perf_counter()
    r = fib_rec(n)
    e = time.perf_counter() - s
    return r, f"{e:.8f}"

def fib_iter(n):
    if n < 0:
        raise ValueError("Negativni cislo")
    a = 0
    b = 1
    t = time.perf_counter()
    for _ in range(n):
        a, b = b, a + b
    e = time.perf_counter() - t
    return a, f"{e:.8f}"

class FibonacciHelper:
    def __init__(self, number):
        self.number = number
    def recursive(self):
        return spocitej_fibonacci(self.number)
    def iterative(self):
        return fib_iter(self.number)
    def same(self):
        x, _ = self.recursive()
        y, _ = self.iterative()
        return x == y

def fibonacci_sequence(m):
    if m < 0:
        return []
    out = []
    for i in range(m+1):
        val, _ = fib_iter(i)
        out.append(val)
    return out

def fibonacci_test_range(a, b):
    if a < 0 or b < 0 or a > b:
        return []
    z = []
    for i in range(a, b+1):
        r1, c1 = spocitej_fibonacci(i)
        r2, c2 = fib_iter(i)
        z.append((i, r1, c1, r2, c2))
    return z

def fib_dummy_calc(n):
    s = 0
    for i in range(n):
        s += i*i
    return s

def fib_plus_dummy(n):
    x, _ = spocitej_fibonacci(n)
    return x + fib_dummy_calc(n)

def fib_matrix_approx(n):
    if n < 0:
        return 0
    return n*n

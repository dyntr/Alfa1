import unittest
import logging

from src.ciselne_operace.fibonacci import fib_rec, spocitej_fibonacci, fib_iter, FibonacciHelper, fibonacci_sequence, \
    fibonacci_test_range, fib_dummy_calc, fib_plus_dummy, fib_matrix_approx

logger = logging.getLogger(__name__)

class TestFibonacci(unittest.TestCase):
    def test_fib_rec_base(self):
        self.assertEqual(fib_rec(0), 0)
        self.assertEqual(fib_rec(1), 1)
        self.assertEqual(fib_rec(2), 1)
        self.assertEqual(fib_rec(5), 5)

    def test_spocitej_fibonacci(self):
        val, t = spocitej_fibonacci(5)
        self.assertEqual(val, 5)
        self.assertTrue(isinstance(t, str))
        val2, t2 = spocitej_fibonacci(0)
        self.assertEqual(val2, 0)

    def test_spocitej_fibonacci_negativni(self):
        with self.assertRaises(ValueError):
            spocitej_fibonacci(-1)

    def test_fib_iter(self):
        val, tm = fib_iter(7)
        self.assertEqual(val, 13)
        self.assertTrue(isinstance(tm, str))

    def test_fib_iter_negativni(self):
        with self.assertRaises(ValueError):
            fib_iter(-10)

    def test_FibonacciHelper(self):
        fh = FibonacciHelper(10)
        r1, c1 = fh.recursive()
        r2, c2 = fh.iterative()
        # fibonacci(10) = 55
        self.assertEqual(r1, 55)
        self.assertEqual(r2, 55)
        self.assertTrue(fh.same())

    def test_fibonacci_sequence(self):
        seq = fibonacci_sequence(5)
        # Očekáváme [0,1,1,2,3,5]
        self.assertEqual(seq, [0,1,1,2,3,5])
        seq_empty = fibonacci_sequence(-5)
        self.assertEqual(seq_empty, [])

    def test_fibonacci_test_range(self):
        # Vrací pole s tuple (i, r1, c1, r2, c2)
        out = fibonacci_test_range(2, 4)
        # Očekáváme 3 řádky: i=2,3,4
        self.assertEqual(len(out), 3)
        # Zkontrolujeme i=2 => fib(2)=1
        i0, r1_0, c1_0, r2_0, c2_0 = out[0]
        self.assertEqual(i0, 2)
        self.assertEqual(r1_0, 1)
        self.assertEqual(r2_0, 1)
        # Když je a>b nebo a<0 => prázdné
        self.assertEqual(fibonacci_test_range(5,3), [])
        self.assertEqual(fibonacci_test_range(-2,2), [])

    def test_fib_dummy_calc(self):
        self.assertEqual(fib_dummy_calc(0), 0)
        self.assertEqual(fib_dummy_calc(1), 0)
        self.assertEqual(fib_dummy_calc(2), 1)
        self.assertEqual(fib_dummy_calc(3), 5)  # i=0,1,2 => 0^2+1^2+2^2=0+1+4=5

    def test_fib_plus_dummy(self):
        # fib(5)=5, dummy(5)=0^2+1^2+2^2+3^2+4^2=30 => 35
        val = fib_plus_dummy(5)
        self.assertEqual(val, 35)

    def test_fib_matrix_approx(self):
        # fib_matrix_approx() vrací n*n
        self.assertEqual(fib_matrix_approx(3), 9)
        self.assertEqual(fib_matrix_approx(-1), 0)

if __name__ == "__main__":
    unittest.main()

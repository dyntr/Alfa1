import unittest
import logging

from src.ciselne_operace.kombinace import spocitej_kombinaci, komb_prohod, KombinacniHelper, kombinace_range, komb_spam, \
    komb_dummy_use, komb_check, komb_multicall

logger = logging.getLogger(__name__)

class TestKombinace(unittest.TestCase):
    def test_spocitej_kombinaci_valid(self):
        r, t = spocitej_kombinaci(5, 3)
        self.assertEqual(r, 10)  # C(5,3)=10
        self.assertTrue(isinstance(t, str))
        r2, t2 = spocitej_kombinaci(8, 2)
        self.assertEqual(r2, 28)  # C(8,2)=28

    def test_spocitej_kombinaci_invalid(self):
        with self.assertRaises(ValueError):
            spocitej_kombinaci(3, 5)  # k>n
        with self.assertRaises(ValueError):
            spocitej_kombinaci(-1, 0)  # n<0
        with self.assertRaises(ValueError):
            spocitej_kombinaci(5, -3)  # k<0

    def test_komb_prohod(self):
        self.assertEqual(komb_prohod(3,5), (5,3))
        self.assertEqual(komb_prohod(5,3), (5,3))
        self.assertEqual(komb_prohod(10,10), (10,10))

    def test_KombinacniHelper(self):
        kh = KombinacniHelper(5,3)
        r, c = kh.compute()
        self.assertEqual(r, 10)
        self.assertTrue(isinstance(c, str))
        self.assertEqual(kh.pair(), (5,3))

    def test_kombinace_range(self):
        rng = kombinace_range(2, 3)
        # (2,0) => C(2,0)=1, (2,1)=2, (2,2)=1, (3,0)=1, (3,1)=3, (3,2)=3, (3,3)=1
        # tzn. 2 => i=2, j=0..2, i=3, j=0..3 => 3+4=7 záznamů
        self.assertEqual(len(rng), 7)
        self.assertEqual(rng[0][:3], (2,0,1))
        self.assertEqual(rng[-1][:3], (3,3,1))

        self.assertEqual(kombinace_range(-1, 2), [])  # a<0 => []
        self.assertEqual(kombinace_range(3, -2), [])  # b<0 => []

    def test_komb_spam(self):
        self.assertEqual(komb_spam(0), 0)
        self.assertEqual(komb_spam(1), 0)
        self.assertEqual(komb_spam(5), sum(range(5)))  # 10

    def test_komb_dummy_use(self):
        # komb_dummy_use(n,k) = (n+k) + komb_spam(n*k)
        # pro n=3,k=2 => (3+2)+komb_spam(6)
        # komb_spam(6)=sum(range(6))=15 => celk.5+15=20
        self.assertEqual(komb_dummy_use(3,2), 20)

    def test_komb_check(self):
        self.assertEqual(komb_check(5,3), 10)
        self.assertIsNone(komb_check(3,5))  # k>n => ValueError => None

    def test_komb_multicall(self):
        seq = [(5,3),(6,2)]
        out = komb_multicall(seq)
        # (5,3) =>10, (6,2)=>C(6,2)=15
        self.assertEqual(len(out), 2)
        self.assertEqual(out[0][0], 5)
        self.assertEqual(out[0][1], 3)
        self.assertEqual(out[0][2], 10)
        self.assertEqual(out[1][2], 15)

if __name__ == "__main__":
    unittest.main()

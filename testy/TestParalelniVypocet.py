import unittest
import math
from src.logika.vypocet_soubeh import ParalelniVypocet


# Pokud se váš soubor jmenuje jinak (např. vypocet_soubeh.py),
# pak: from vypocet_soubeh import ParalelniVypocet

class TestParalelniVypocet(unittest.TestCase):
    def test_faktorial_sekvence(self):
        p = ParalelniVypocet([3,5], "faktorial")
        vysl, cas = p.vypocet_sekvence()
        self.assertEqual(len(vysl), 2)
        # Očekáváme factorial(3)=6, factorial(5)=120
        # Klíče by měly být ve formátu "index:hodnota"
        # Např. "0:3" a "1:5"
        self.assertIn("0:3", vysl)
        self.assertIn("1:5", vysl)
        self.assertEqual(vysl["0:3"]["vysledek"], 6)
        self.assertEqual(vysl["1:5"]["vysledek"], 120)
        self.assertTrue(float(cas) >= 0.0)

    def test_faktorial_vlakna(self):
        p = ParalelniVypocet([3,5], "faktorial")
        vysl, cas = p.vypocet_vlakna()
        self.assertEqual(len(vysl), 2)
        self.assertIn("0:3", vysl)
        self.assertIn("1:5", vysl)
        self.assertEqual(vysl["0:3"]["vysledek"], 6)
        self.assertEqual(vysl["1:5"]["vysledek"], 120)

    def test_faktorial_procesy(self):
        p = ParalelniVypocet([3,5], "faktorial")
        vysl, cas = p.vypocet_procesy()
        self.assertEqual(len(vysl), 2)
        self.assertIn("0:3", vysl)
        self.assertIn("1:5", vysl)
        self.assertEqual(vysl["0:3"]["vysledek"], 6)
        self.assertEqual(vysl["1:5"]["vysledek"], 120)

    def test_fibonacci_sekvence(self):
        p = ParalelniVypocet([5,7], "fibonacci")
        vysl, cas = p.vypocet_sekvence()
        self.assertEqual(len(vysl), 2)
        # fibonacci(5) = 5, fibonacci(7) = 13
        self.assertIn("0:5", vysl)
        self.assertIn("1:7", vysl)
        self.assertEqual(vysl["0:5"]["vysledek"], 5)
        self.assertEqual(vysl["1:7"]["vysledek"], 13)

    def test_fibonacci_vlakna(self):
        p = ParalelniVypocet([5,7], "fibonacci")
        vysl, cas = p.vypocet_vlakna()
        self.assertEqual(len(vysl), 2)
        self.assertIn("0:5", vysl)
        self.assertIn("1:7", vysl)
        self.assertEqual(vysl["0:5"]["vysledek"], 5)
        self.assertEqual(vysl["1:7"]["vysledek"], 13)

    def test_fibonacci_procesy(self):
        p = ParalelniVypocet([5,7], "fibonacci")
        vysl, cas = p.vypocet_procesy()
        self.assertEqual(len(vysl), 2)
        self.assertIn("0:5", vysl)
        self.assertIn("1:7", vysl)
        self.assertEqual(vysl["0:5"]["vysledek"], 5)
        self.assertEqual(vysl["1:7"]["vysledek"], 13)

    def test_kombinace_sekvence(self):
        # Zadame ctyri cisla, budou interpretovany jako (5,3) a (8,2)
        p = ParalelniVypocet([5,3,8,2], "kombinace")
        vysl, cas = p.vypocet_sekvence()
        self.assertEqual(len(vysl), 2)
        # C(5,3) = 10, C(8,2) = 28
        # Klic "0:(5, 3)" a "1:(8, 2)"
        self.assertIn("0:(5, 3)", vysl)
        self.assertIn("1:(8, 2)", vysl)
        self.assertEqual(vysl["0:(5, 3)"]["vysledek"], 10)
        self.assertEqual(vysl["1:(8, 2)"]["vysledek"], 28)

    def test_kombinace_vlakna(self):
        p = ParalelniVypocet([5,3,8,2], "kombinace")
        vysl, cas = p.vypocet_vlakna()
        self.assertEqual(len(vysl), 2)
        self.assertIn("0:(5, 3)", vysl)
        self.assertIn("1:(8, 2)", vysl)
        self.assertEqual(vysl["0:(5, 3)"]["vysledek"], 10)
        self.assertEqual(vysl["1:(8, 2)"]["vysledek"], 28)

    def test_kombinace_procesy(self):
        p = ParalelniVypocet([5,3,8,2], "kombinace")
        vysl, cas = p.vypocet_procesy()
        self.assertEqual(len(vysl), 2)
        self.assertIn("0:(5, 3)", vysl)
        self.assertIn("1:(8, 2)", vysl)
        self.assertEqual(vysl["0:(5, 3)"]["vysledek"], 10)
        self.assertEqual(vysl["1:(8, 2)"]["vysledek"], 28)

if __name__ == "__main__":
    unittest.main()

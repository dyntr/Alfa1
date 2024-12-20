import unittest
import os
import json
import logging

from src.logika.spravce_nastaveni import SpravceNastaveni, DEFAULT_CONFIG

logger = logging.getLogger(__name__)

class TestSpravceNastaveni(unittest.TestCase):
    def setUp(self):
        self.test_file = "data/test_nastaveni.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.spravce = SpravceNastaveni(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_neexistujici_soubor_vytvori_vychozi(self):
        cisla, typ = self.spravce.nacti_nastaveni()
        self.assertEqual(cisla, DEFAULT_CONFIG["cisla"])
        self.assertEqual(typ, DEFAULT_CONFIG["typ_vypoctu"])
        self.assertTrue(os.path.exists(self.test_file))

    def test_prazdny_soubor_vytvori_vychozi(self):
        os.makedirs("data", exist_ok=True)
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("")  # prázdný obsah
        cisla, typ = self.spravce.nacti_nastaveni()
        self.assertEqual(cisla, DEFAULT_CONFIG["cisla"])
        self.assertEqual(typ, DEFAULT_CONFIG["typ_vypoctu"])

    def test_korektni_konfigurace_je_nactena(self):
        os.makedirs("data", exist_ok=True)
        config_data = {"cisla": [1,2,3], "typ_vypoctu": "fibonacci"}
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
        cisla, typ = self.spravce.nacti_nastaveni()
        self.assertEqual(cisla, [1,2,3])
        self.assertEqual(typ, "fibonacci")

    def test_neznamy_typ_se_nastavi_na_vychozi(self):
        os.makedirs("data", exist_ok=True)
        config_data = {"cisla": [10,20], "typ_vypoctu": "neznamy"}
        with open(self.test_file, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
        cisla, typ = self.spravce.nacti_nastaveni()
        self.assertEqual(cisla, [10,20])
        self.assertEqual(typ, "faktorial")

    def test_chovani_metod(self):
        self.spravce.custom_method()
        self.assertIn("some_data", self.spravce.extra_data)
        self.spravce.set_prepared(True)
        self.assertTrue(self.spravce.check_prepared())

if __name__ == "__main__":
    unittest.main()

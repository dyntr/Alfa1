import unittest
import os
import json
import logging

from src.logika.uloziste import UlozisteVysledku

logger = logging.getLogger(__name__)

class TestUlozisteVysledku(unittest.TestCase):
    def setUp(self):
        self.test_file = "data/test_vysledky.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.uloziste = UlozisteVysledku(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_prvotni_soubor_neexistuje_vytvori_se(self):
        data = self.uloziste.nacti_vse()
        self.assertIn("polozky", data)
        self.assertEqual(len(data["polozky"]), 0)
        self.assertTrue(os.path.exists(self.test_file))

    def test_uloz_dva_zaznamy(self):
        d1 = {"typ": "faktorial", "sekvencni": {}}
        d2 = {"typ": "fibonacci", "sekvencni": {}}
        self.uloziste.uloz(d1)
        self.uloziste.uloz(d2)
        with open(self.test_file, "r", encoding="utf-8") as f:
            obsah = json.load(f)
        self.assertIn("polozky", obsah)
        self.assertEqual(len(obsah["polozky"]), 2)
        self.assertEqual(obsah["polozky"][0]["typ"], "faktorial")
        self.assertEqual(obsah["polozky"][1]["typ"], "fibonacci")

    def test_vymaz_vse(self):
        d1 = {"typ": "faktorial"}
        d2 = {"typ": "fibonacci"}
        self.uloziste.uloz(d1)
        self.uloziste.uloz(d2)
        self.uloziste.vymaz_vse()
        result = self.uloziste.nacti_vse()
        self.assertEqual(len(result["polozky"]), 0)

    def test_aktualizuj_zaznam(self):
        d1 = {"typ":"faktorial","sekvencni":{}}
        self.uloziste.uloz(d1)
        d2 = {"typ":"fibonacci","sekvencni":{}}
        self.uloziste.uloz(d2)
        veskere = self.uloziste.nacti_vse()
        self.assertEqual(len(veskere["polozky"]), 2)

        id_ke_zmene = 1
        nove_udaje = {"typ":"kombinace"}
        self.uloziste.aktualizuj_zaznam(id_ke_zmene, nove_udaje)

        updated = self.uloziste.nacti_vse()
        polozky = updated["polozky"]
        self.assertEqual(polozky[0]["id"], 1)
        self.assertEqual(polozky[0]["typ"], "kombinace")
        self.assertEqual(polozky[1]["typ"], "fibonacci")

    def test_vypis_vse(self):
        d1 = {"typ":"faktorial"}
        self.uloziste.uloz(d1)
        # jen kontrola, zda volání proběhne bez chyby
        self.uloziste.vypis_vse()

if __name__ == "__main__":
    unittest.main()

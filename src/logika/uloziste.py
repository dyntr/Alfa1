import json
import os
import logging

logger = logging.getLogger(__name__)

class UlozisteVysledku:
    def __init__(self, cesta="data/vysledky.json"):
        self.cesta = cesta
        self.cache = None

    def _nacti_data(self):
        if not os.path.exists(self.cesta):
            d = os.path.dirname(self.cesta)
            if d and not os.path.exists(d):
                os.makedirs(d, exist_ok=True)
            return {"polozky": []}
        try:
            with open(self.cesta, "r", encoding="utf-8") as f:
                txt = f.read().strip()
                if not txt:
                    return {"polozky": []}
                return json.loads(txt)
        except Exception as e:
            logger.error(f"Chyba pri cteni souboru {self.cesta}: {e}")
            return {"polozky": []}

    def _uloz_data(self, data):
        try:
            with open(self.cesta, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info(f"Data uspesne zapsana do {self.cesta}")
            print(f"Data uspesne zapsana do {self.cesta}")
        except Exception as e:
            logger.error(f"Chyba pri zapisu do {self.cesta}: {e}")
            print(f"Chyba pri zapisu do {self.cesta}: {e}")

    def _next_id(self, data):
        if "polozky" not in data or not isinstance(data["polozky"], list):
            return 1
        return len(data["polozky"]) + 1

    def uloz(self, vysledky):
        data = self._nacti_data()
        if "polozky" not in data:
            data["polozky"] = []
        i = self._next_id(data)
        novy = {"id": i, **vysledky}
        data["polozky"].append(novy)
        self._uloz_data(data)
        logger.info(f"Zaznam s id={i} ulozen do {self.cesta}")
        print(f"Zaznam s id={i} ulozen do {self.cesta}")

    def vymaz_vse(self):
        prazdny = {"polozky": []}
        self._uloz_data(prazdny)
        logger.warning("Vsechny zaznamy smazany")

    def nacti_vse(self):
        self.cache = self._nacti_data()
        return self.cache

    def vypis_vse(self):
        if self.cache is None:
            self.cache = self._nacti_data()
        for item in self.cache.get("polozky", []):
            print(f"ID={item.get('id')} | zbytek={item}")

    def aktualizuj_zaznam(self, zadane_id, nove_udaje):
        d = self._nacti_data()
        if "polozky" not in d:
            d["polozky"] = []
        nalezen = False
        for rec in d["polozky"]:
            if rec.get("id") == zadane_id:
                for k,v in nove_udaje.items():
                    rec[k] = v
                nalezen = True
                break
        if nalezen:
            self._uloz_data(d)
            logger.info(f"Aktualizovan id={zadane_id}")
        else:
            logger.warning(f"Nenalezen id={zadane_id}")

def test_uloziste():
    u = UlozisteVysledku("data/test_vysledky.json")
    d1 = {"typ":"faktorial","sekvencni":{}}
    u.uloz(d1)
    d2 = {"typ":"fibonacci","sekvencni":{}}
    u.uloz(d2)
    x = u.nacti_vse()
    u.vypis_vse()
    u.vymaz_vse()
    return x

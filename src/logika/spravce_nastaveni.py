import json
import os
import logging

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {"cisla": [5, 3, 7], "typ_vypoctu": "faktorial"}

class SpravceNastaveni:
    def __init__(self, cesta="data/nastaveni.json"):
        self.cesta = cesta
        self.extra_data = []
        self.prepared = False

    def oprav_vychozi(self):
        d = os.path.dirname(self.cesta)
        if d and not os.path.exists(d):
            os.makedirs(d, exist_ok=True)
        with open(self.cesta, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
        logger.info(f"Vytvoren soubor s default configem: {self.cesta}")
        return DEFAULT_CONFIG["cisla"], DEFAULT_CONFIG["typ_vypoctu"]

    def nacti_nastaveni(self):
        if not os.path.exists(self.cesta):
            logger.warning(f"Soubor {self.cesta} neexistuje, vytvarim default.")
            return self.oprav_vychozi()
        try:
            with open(self.cesta, "r", encoding="utf-8") as f:
                obsah = f.read().strip()
                if not obsah:
                    logger.warning(f"Soubor {self.cesta} je prazdny, vytvarim default.")
                    return self.oprav_vychozi()
                jdata = json.loads(obsah)
            if "cisla" not in jdata or not isinstance(jdata["cisla"], list):
                logger.warning(f"V souboru {self.cesta} chybi 'cisla' nebo neni list, vytvarim default.")
                return self.oprav_vychozi()
            c = jdata.get("cisla", [])
            t = jdata.get("typ_vypoctu", "faktorial")
            povolene = ["faktorial", "fibonacci", "kombinace"]
            if t not in povolene:
                logger.warning(f"typ_vypoctu {t} neni povoleny, nastavuje se faktorial.")
                t = "faktorial"
            logger.info(f"Nacteno nastaveni: cisla={c}, typ={t}")
            return c, t
        except Exception as e:
            logger.error(f"Chyba pri nacitani {self.cesta}: {e}")
            return self.oprav_vychozi()

    def custom_method(self):
        self.extra_data.append("some_data")
        logger.debug("Pridano do extra_data")

    def check_prepared(self):
        return self.prepared

    def set_prepared(self, val):
        self.prepared = bool(val)

def test_spravce():
    s = SpravceNastaveni("data/test_nastaveni.json")
    cisla, typ = s.nacti_nastaveni()
    logger.info(f"Test spravce: {cisla}, {typ}")
    s.custom_method()
    s.set_prepared(True)
    return s.check_prepared()

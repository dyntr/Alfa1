import sys
import logging
import os
from src.logika.spravce_nastaveni import SpravceNastaveni
from src.logika.vypocet_soubeh import ParalelniVypocet
from src.logika.uloziste import UlozisteVysledku

logger = logging.getLogger()
logger.setLevel(logging.INFO)

if not os.path.exists("data"):
    os.makedirs("data", exist_ok=True)

fh = logging.FileHandler("data/app.log", mode="a", encoding="utf-8")
fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(fmt)
sh = logging.StreamHandler(sys.stdout)
logger.addHandler(sh)
logger.addHandler(fh)

def main():
    print("1 - Config")
    print("2 - Console")
    vyber = input("Zadejte volbu: ")
    if vyber.strip() == "2":
        txt = input("Zadejte cisla (lze i s carkami): ")
        txt = txt.replace(",", " ")
        try:
            arr = list(map(int, txt.split()))
        except:
            print("Chyba ve vstupu")
            return
        typ = input("Zadejte typ (faktorial/fibonacci/kombinace): ")
        if typ not in ["faktorial","fibonacci","kombinace"]:
            typ = "faktorial"
        paral = ParalelniVypocet(arr, typ)
    else:
        sn = SpravceNastaveni("data/nastaveni.json")
        c, t = sn.nacti_nastaveni()
        paral = ParalelniVypocet(c, t)

    r1, c1 = paral.vypocet_sekvence()
    r2, c2 = paral.vypocet_vlakna()
    r3, c3 = paral.vypocet_procesy()

    print("Sekvencne:", r1, c1)
    print("Vlakna:", r2, c2)
    print("Procesy:", r3, c3)

    u = UlozisteVysledku("data/vysledky.json")
    vysl = {
        "typ_vypoctu": paral.typ,
        "sekvencni": {"vysledky": r1, "cas_celkem": c1},
        "vlakna": {"vysledky": r2, "cas_celkem": c2},
        "procesy": {"vysledky": r3, "cas_celkem": c3}
    }
    u.uloz(vysl)
    print("Hotovo.")

def ukaz_logy():
    try:
        with open("data/app.log","r",encoding="utf-8") as ff:
            for line in ff:
                print(line.rstrip())
    except:
        print("Log app.log nenalezen")

def test_main():
    pass

if __name__=="__main__":
    main()

import time
import logging
from threading import Thread
from multiprocessing import Pool
from src.ciselne_operace.faktorial import spocitej_faktorial
from src.ciselne_operace.fibonacci import spocitej_fibonacci
from src.ciselne_operace.kombinace import spocitej_kombinaci

logger = logging.getLogger(__name__)

class ParalelniVypocet:
    def __init__(self, vstup, typ="faktorial"):
        self.typ = typ
        if self.typ == "kombinace":
            pary = []
            i = 0
            while i < len(vstup):
                n = vstup[i]
                k = 0
                if i + 1 < len(vstup):
                    k = vstup[i + 1]
                if k > n:
                    n, k = k, n
                pary.append((n, k))
                i += 2
            self.data = pary
        else:
            self.data = vstup

    def _vyber(self, val):
        if self.typ == "fibonacci":
            return spocitej_fibonacci(val)
        elif self.typ == "kombinace":
            return spocitej_kombinaci(val[0], val[1])
        else:
            return spocitej_faktorial(val)

    def vypocet_sekvence(self):
        vysledky = {}
        soucet_casu = 0.0
        for idx, prvek in enumerate(self.data):
            v, c = self._vyber(prvek)
            key = f"{idx}:{prvek}"
            vysledky[key] = {"vysledek": v, "cas": c}
            soucet_casu += float(c)
        return vysledky, f"{soucet_casu:.8f}"

    def vypocet_vlakna(self):
        vysledky = {}
        casy = {}

        def vlakno_fce(idx, hodnota):
            v, c = self._vyber(hodnota)
            key = f"{idx}:{hodnota}"
            vysledky[key] = v
            casy[key] = float(c)

        threads = []
        for i, val in enumerate(self.data):
            t = Thread(target=vlakno_fce, args=(i, val))
            threads.append(t)
            t.start()

        for th in threads:
            th.join()

        soucet = sum(casy.values())
        final_dict = {}
        for k in vysledky:
            final_dict[k] = {
                "vysledek": vysledky[k],
                "cas": f"{casy[k]:.8f}"
            }
        return final_dict, f"{soucet:.8f}"

    def vypocet_procesy(self):
        start = time.perf_counter()
        with Pool() as pool:
            vysledky_list = pool.map(self._vyber, self.data)
        elapsed = time.perf_counter() - start

        vysledky = {}
        for idx, (val) in enumerate(self.data):
            r, c = vysledky_list[idx]
            key = f"{idx}:{val}"
            vysledky[key] = {"vysledek": r, "cas": c}

        return vysledky, f"{elapsed:.8f}"

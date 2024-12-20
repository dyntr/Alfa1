# **Školní projekt: Paralelní Výpočty**

## **Autor:** Patrick Dyntr

**Škola:** SPŠE Ječná  
**Předmět:** Programování a algoritmy  

---

## **1. Název projektu**

**Paralelní výpočty pro faktoriál, Fibonacciho posloupnost a kombinace**

---

## **2. Úvod**

Tento projekt byl vytvořen jako školní úloha pro demonstraci použití paralelních výpočtů v programování. Cílem projektu je implementace a porovnání výpočetních metod (sekvenční, vláknové a procesové) pro výpočet matematických operací, jako jsou faktoriál, Fibonacciho posloupnost a kombinace. Projekt se zaměřuje na efektivitu výpočtů a jejich využití v různých situacích, kde je třeba zpracovávat velké množství dat.

Projekt zahrnuje moduly pro zpracování vstupních dat, ukládání výsledků a testování různých přístupů k výpočtům. Navíc je projekt doplněn o sadu jednotkových testů, které zajišťují správnost výstupů. Součástí projektu je také přehled logovacích mechanismů a práce s konfigurací, což přispívá k lepší spravovatelnosti kódu a snadné analýze chyb.

---

## **3. Požadavky**

- **Programovací jazyk:** Python 3.12
- **Framework pro testování:** `unittest`
- **Knihovny:** `json`, `os`, `sys`, `logging`, `time`, `math`, `threading`, `multiprocessing`
- **Platforma:** Windows / macOS / Linux
- **Organizace projektu:**
  - Zdrojové kódy rozděleny do modulů pro lepší přehlednost a znovupoužitelnost.
  - Testy organizované ve zvláštní složce `testy`.
  - Výsledky a konfigurace ukládány do složky `data`.
  - Zajištění logování událostí pro snadnou diagnostiku a ladění.

---

## **4. Popis projektu**

### **4.1 Funkcionalita**

Projekt umožňuje provádět výpočty:

- **Faktoriál:** Výpočet faktoriálu zadaného čísla.
- **Fibonacciho posloupnost:** Výpočet n-tého členu Fibonacciho posloupnosti.
- **Kombinace:** Výpočet kombinací pro dané hodnoty n a k.
- **Testování výkonu:** Porovnání rychlostí jednotlivých metod.
- **Ukládání výsledků:** Uložení výpočtů do souboru JSON.

### **4.2 Metody výpočtu**

1. **Sekvenční výpočet:** Postupné zpracování vstupů jeden po druhém. Tento přístup je nejjednodušší, ale nejpomalejší.
2. **Vláknové výpočty:** Paralelní zpracování využívající více vláken. Tento přístup je vhodný pro výpočty s menšími úlohami.
3. **Procesové výpočty:** Paralelní zpracování pomocí samostatných procesů. Tento přístup je vhodný pro výpočty s většími datovými sadami.

Každý typ výpočtu je porovnán z hlediska rychlosti a efektivity, což umožňuje uživateli vybrat nejvhodnější metodu pro daný úkol.

### **4.3 Struktura projektu**

Projekt je rozdělen do následujících složek:

- **src/** - hlavní zdrojové kódy:

  - `main.py` – spouštěcí skript.
  - `logika/` – logika pro zpracování vstupů, ukládání dat a paralelní výpočty.
  - `ciselne_operace/` – implementace matematických funkcí.

- **data/** - ukládání nastavení a výsledků:

  - `nastaveni.json` – konfigurační soubor s výchozím nastavením.
  - `vysledky.json` – uložené výsledky výpočtů.
  - `app.log` – logovací soubor.

- **testy/** - testovací skripty:

  - Pokrývají různé části projektu, včetně funkcí pro výpočty, ukládání dat a nastavení.

- **__pycache__/** - kompilované soubory Pythonu (automaticky generované).

---

## **5. Testy a úspěšnost**

### **5.1 Testovací pokrytí**

Testy ověřují:

1. Správnost výpočtů pro faktoriál, Fibonacciho posloupnost a kombinace.
2. Správnost ukládání, načítání a mazání výsledků.
3. Funkčnost správy konfigurace.
4. Chybové stavy a okrajové případy.
5. Výkonnostní testy pro různé vstupy a konfigurace.

### **5.2 Seznam testů a výsledky**

- **TestFaktorial.py** – Všechny testy prošly úspěšně.
- **TestFibonacci.py** – Všechny testy prošly úspěšně.
- **TestKombinace.py** – Všechny testy prošly úspěšně.
- **TestUlozisteVysledku.py** – Všechny testy prošly úspěšně.
- **TestSpravceNastaveni.py** – Všechny testy prošly úspěšně.
- **TestParalelniVypocet.py** – Všechny testy prošly úspěšně.

---

## **6. Závěr**

Projekt poskytuje komplexní pohled na implementaci a optimalizaci výpočtů v Pythonu. Důraz byl kladen na správnost, testovatelnost a efektivitu kódu. Výsledky ukazují, že pro různé typy úloh lze využít různé přístupy k optimalizaci výpočtů. Díky jednotkovým testům je zajištěna vysoká spolehlivost a přesnost výpočtů.

---

## **7. Odkazy**

- Python 3.12 Dokumentace: [https://docs.python.org/3/](https://docs.python.org/3/)
- Unittest Framework: [https://docs.python.org/3/library/unittest.html](https://docs.python.org/3/library/unittest.html)


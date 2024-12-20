# Dokumentace k projektu: Paralelní zpracování souborů na Discord

## 1. Úvod
Projekt se zaměřuje na dekompozici problému nahrávání a stahování souborů na Discord pomocí paralelního zpracování. Cílem projektu je umožnit efektivní práci s velkými soubory, které jsou rozděleny na menší části a zpracovány paralelně pomocí procesů.

Hlavní funkce projektu zahrnují:
- Nahrávání souborů na Discord.
- Rozdělování velkých souborů na menší části.
- Skládání rozdělených částí zpět do původního souboru.
- Paralelní zpracování úloh pomocí fronty.
- Uživatelské rozhraní pro ovládání programu.

---

## 2. Analýza
### Teoretické základy
Paralelní zpracování je metoda rozdělení výpočtu nebo úloh na menší části, které mohou být zpracovány současně. Využití paralelního zpracování přináší:
1. **Zrychlení zpracování** - Využitím více jader nebo procesů.
2. **Optimalizaci zdrojů** - Snížení zátěže na jednotlivé procesory.
3. **Efektivní práci se soubory** - Umožňuje zpracovávat velké soubory, které by jinak překročily limity nahrávání.

Tento projekt využívá paralelní zpracování prostřednictvím modulu `multiprocessing` v Pythonu, který umožňuje vytváření samostatných procesů a sdílení dat mezi nimi.

---

## 3. Implementace a testování
### Použité technologie
- **Python 3.9+** - Programovací jazyk pro implementaci logiky.
- **Discord API** - Pro komunikaci s Discord servery.
- **PyQt5** - Pro vytvoření grafického uživatelského rozhraní (GUI).
- **aiohttp** - Pro asynchronní stahování souborů.
- **Multiprocessing** - Pro paralelní zpracování úloh.

### Architektura programu
Program je rozdělen do tří hlavních komponent:
1. **Logger** - Spravuje logování chyb, varování a běžných informací.
2. **FileUploader** - Zajišťuje nahrávání, rozdělování a skládání souborů.
3. **GUI aplikace** - Umožňuje uživatelskou interakci s programem.

Každá komponenta je oddělená a komunikuje prostřednictvím sdílených front pro zasílání úloh a výsledků.

### Funkcionality
- **Rozdělování souborů:**
  Soubor je rozdělen na části dle velikostního limitu Discordu (25 MB).
- **Skládání souborů:**
  Rozdělené části lze stáhnout a znovu spojit do původního souboru.
- **Paralelní zpracování:**
  Využití fronty k zasílání úloh mezi procesy.
- **Asynchronní komunikace:**
  Pro efektivní práci se síťovými požadavky.

### Testování
1. **Jednotkové testy** - Otestování jednotlivých funkcí (např. rozdělování souborů).
2. **Zátěžové testy** - Testování práce s velkými soubory (až 500 MB).
3. **Integrační testy** - Ověření, že všechny komponenty spolupracují správně.

---

## 4. Dokumentace a reporty
### Popis funkcionalit
#### GUI aplikace
1. Výběr souboru pro nahrání.
2. Zobrazení seznamu již nahraných souborů.
3. Stahování vybraných souborů.

#### Paralelní zpracování
Program využívá více procesů pro zpracování požadavků, což zajišťuje rychlejší odezvu a schopnost pracovat s více soubory najednou.

#### Logování a validace
Všechny operace jsou logovány. Program obsahuje ochranu proti nevalidním vstupům (kontrola velikosti, existence souborů).

### Výstupy testování
| Testovací scénář                  | Výstup               | Výsledek   |
|-----------------------------------|----------------------|-----------|
| Rozdělení souboru (100 MB)        | 4 části po 25 MB     | Úspěch    |
| Skládání souboru                  | Obnovený původní soubor | Úspěch    |
| Upload na Discord (100 MB)        | Rozdělené části nahrány | Úspěch    |
| Stahování a rekonstrukce souboru  | Spojené části odpovídají originálu | Úspěch    |

### Zdroje
- [Python multiprocessing](https://docs.python.org/3/library/multiprocessing.html)
- [Discord API dokumentace](https://discord.com/developers/docs/intro)
- [PyQt5 dokumentace](https://doc.qt.io/qtforpython/)
- Konzultace s učiteli PV.

---

## 5. Nasazení
### Struktura souborů
```
project/
|-- src/
|   |-- bot.py
|   |-- logger.py
|   |-- config.py
|-- test/
|   |-- test_logger.py
|-- doc/
|   |-- dokumentace.md
|-- logs/
|-- downloads/
|-- split_files/
|-- requirements.txt
|-- README.md
```

### Instalace a spuštění
1. **Závislosti:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Konfigurace prostředí:**
   Vytvořte soubor `.env` a nastavte:
   ```
   DISCORD_TOKEN=váš_token
   UPLOAD_CHANNEL_ID=123456789
   DISCORD_UPLOAD_LIMIT=26214400
   ```
3. **Spuštění aplikace:**
   ```bash
   python main.py
   ```

---

## Závěr
Projekt ukazuje praktické využití paralelního zpracování pro práci se soubory na Discordu. Využívá asynchronní komunikaci, víceprocesovou architekturu a moderní nástroje, čímž splňuje všechny zadané požadavky. Program je snadno rozšiřitelný a připravený na další vývoj.


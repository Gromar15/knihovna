# Půjčovna knih – Flask prototyp

## Spuštění

```bash
pip install -r requirements.txt
python app.py
```

Otevři prohlížeč na `http://127.0.0.1:5000`

## Struktura

```
knihovna/
├── app.py                  # Flask routy & byznys logika
├── models.py               # SQLAlchemy modely (Book, Member, Loan)
├── requirements.txt
├── README.md
├── static/
│   ├── css/
│   │   └── style.css       # Vlastní styly (volitelné)
│   └── js/
│       └── main.js         # Vlastní skripty (volitelné)
└── templates/
    ├── _base.html          # Základní layout (navbar, flash zprávy)
    ├── index.html          # Dashboard – seznam knih
    ├── clenove.html        # Seznam členů
    ├── pridat_clena.html   # Formulář nového člena
    ├── nova_pujcka.html    # Formulář výpůjčky
    └── pujcky.html         # Přehled výpůjček
```

## Funkce

- ✅ Výpůjčka pouze dostupné knihy
- ✅ Vrácení = dnešní datum + stav knihy zpět na dostupná
- ✅ Ukázková data při prvním spuštění
- ✅ Flash zprávy pro všechny akce

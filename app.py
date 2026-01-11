from flask import Flask, render_template, request
import pandas as pd
import re

app = Flask(__name__)

# ===== KONFIGURACJA =====
PLIK_EXCEL = "data.xlsx"
KOLUMNA_PROJEKT = "PROJEKT"
# ========================

# Wczytanie Excela
df = pd.read_excel(PLIK_EXCEL)

# Oryginalna kolumna jako tekst
df[KOLUMNA_PROJEKT] = df[KOLUMNA_PROJEKT].astype(str)

# Kolumna techniczna do wyszukiwania
def normalizuj(txt):
    txt = txt.lower()
    txt = re.sub(r"[()\s]", "", txt)  # usuń spacje i nawiasy
    return txt

df["__search__"] = df[KOLUMNA_PROJEKT].apply(normalizuj)

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "").strip().lower()
    wynik = []

    if query:
        query_norm = normalizuj(query)
        wynik = df[df["__search__"].str.contains(query_norm, na=False)]
        wynik = wynik.to_dict(orient="records")

    return render_template("index.html", wynik=wynik, query=query)

if __name__ == "__main__":
    app.run(debug=True)


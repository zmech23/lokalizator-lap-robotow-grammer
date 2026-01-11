from flask import Flask, render_template, request
import pandas as pd
import re

app = Flask(__name__)

# ====== KONFIGURACJA ======
PLIK_EXCEL = "data.xlsx"     # nazwa pliku Excel
KOLUMNA_PROJEKT = "PROJEKT"  # MUSI BYĆ DOKŁADNIE jak w Excelu
# ==========================

# Wczytanie Excela
df = pd.read_excel(PLIK_EXCEL)

# Upewniamy się, że kolumna istnieje
df[KOLUMNA_PROJEKT] = df[KOLUMNA_PROJEKT].astype(str)

# Tworzymy kolumnę techniczną do wyszukiwania
def normalizuj(txt):
    txt = txt.lower()
    txt = re.sub(r"[()\s]", "", txt)  # usuń spacje i nawiasy
    return txt

df["__search__"] = df[KOLUMNA_PROJEKT].apply(normalizuj)

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "").strip()
    wynik = []

    if query:
        q_norm = normalizuj(query)

        mask = df["__search__"].str.contains(q_norm, na=False)
        wynik = df[mask].to_dict(orient="records")

    return render_template("index.html", wynik=wynik, query=query)

if __name__ == "__main__":
    app.run(debug=True)


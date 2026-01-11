from flask import Flask, render_template, request
import pandas as pd
import re

app = Flask(__name__)

PLIK_EXCEL = "data.xlsx"

# ===== WCZYTANIE =====
df = pd.read_excel(PLIK_EXCEL)

# automatycznie znajdź kolumnę projektu
KOLUMNA_PROJEKT = None
for col in df.columns:
    if "projekt" in col.lower():
        KOLUMNA_PROJEKT = col
        break

if KOLUMNA_PROJEKT is None:
    raise Exception("Brak kolumny z projektem")

df[KOLUMNA_PROJEKT] = df[KOLUMNA_PROJEKT].astype(str)

# ===== FUNKCJE =====
def wyciagnij_kod(txt):
    txt = txt.lower()
    match = re.search(r"s\d+", txt)
    return match.group(0) if match else ""

df["__kod__"] = df[KOLUMNA_PROJEKT].apply(wyciagnij_kod)

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "").strip().lower()
    wynik = []

    if query:
        # użytkownik wpisuje np. s11777
        kod = wyciagnij_kod(query)
        if kod:
            mask = df["__kod__"] == kod
            wynik = df[mask].to_dict(orient="records")

    return render_template("index.html", wynik=wynik, query=query)

if __name__ == "__main__":
    app.run(debug=True)


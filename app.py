from flask import Flask, render_template, request
import pandas as pd
import re

app = Flask(__name__)

# === KONFIGURACJA ===
EXCEL_FILE = "data.xlsx"
KOLUMNA_PROJEKT = "PROJEKT"

# === WCZYTANIE DANYCH ===
df = pd.read_excel(EXCEL_FILE)
df[KOLUMNA_PROJEKT] = df[KOLUMNA_PROJEKT].astype(str)

# normalizacja tekstu (usuwa spacje, nawiasy, znaki specjalne)
def normalizuj(txt):
    txt = txt.lower()
    txt = re.sub(r"\s+", "", txt)
    txt = re.sub(r"[()]", "", txt)
    return txt

df["_norm"] = df[KOLUMNA_PROJEKT].apply(normalizuj)

# === ROUTE ===
@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "").strip()
    results = []

    if query:
        q_norm = normalizuj(query)
        mask = df["_norm"].str.contains(q_norm, na=False)
        results = df[mask].drop(columns="_norm").to_dict(orient="records")

    return render_template(
        "index.html",
        query=query,
        results=results
    )

# === START ===
if __name__ == "__main__":
    app.run(debug=True)

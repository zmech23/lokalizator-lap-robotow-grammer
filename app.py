from flask import Flask, render_template, request
import pandas as pd
import re

app = Flask(__name__)

PLIK_EXCEL = "data.xlsx"
KOLUMNA_PROJEKT = "PROJEKT"

df = pd.read_excel(PLIK_EXCEL)
df[KOLUMNA_PROJEKT] = df[KOLUMNA_PROJEKT].astype(str)

def normalizuj(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]", "", text)  # usuwa spacje, nawiasy itd.
    return text

# kolumna pomocnicza do wyszukiwania
df["__norm"] = df[KOLUMNA_PROJEKT].apply(normalizuj)

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "").strip()
    wynik = []

    if query:
        q_norm = normalizuj(query)
        mask = df["__norm"].str.contains(q_norm, na=False)
        wynik = df[mask].drop(columns="__norm").to_dict(orient="records")

    return render_template("index.html", wynik=wynik, query=query)

if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask, render_template, request
import pandas as pd
import re

app = Flask(__name__)

# Wczytaj Excel
df = pd.read_excel("data.xlsx")

# Weź PIERWSZĄ kolumnę z Excela (bez zgadywania nazw)
KOLUMNA = df.columns[0]

# Zamień na tekst
df[KOLUMNA] = df[KOLUMNA].astype(str)

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w]", "", text)
    return text

@app.route("/", methods=["GET", "POST"])
def index():
    wynik = []
    query = ""

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        query_norm = normalize(query)

        df["projekt_norm"] = df[KOLUMNA].apply(normalize)

        # 🔑 startswith → wyszukiwanie bazowe projektu
        wynik = df[df["projekt_norm"].str.startswith(query_norm)]
        wynik = wynik.to_dict(orient="records")

    return render_template("index.html", wynik=wynik, query=query)

if __name__ == "__main__":
    app.run(debug=True)

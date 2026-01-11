from flask import Flask, render_template, request
import pandas as pd
import re

app = Flask(__name__)

# wczytanie danych
df = pd.read_excel("data.xlsx")
df["projekt"] = df["projekt"].astype(str)

def normalize(text):
    """
    Usuwa spacje, nawiasy i zamienia na małe litery
    """
    text = text.lower()
    text = re.sub(r"[^\w]", "", text)  # usuwa spacje, nawiasy itp.
    return text

@app.route("/", methods=["GET", "POST"])
def index():
    wynik = []
    query = ""

    if request.method == "POST":
        query = request.form.get("query", "").strip().lower()
        query_norm = normalize(query)

        df["projekt_norm"] = df["projekt"].apply(normalize)

        wynik = df[df["projekt_norm"].str.startswith(query_norm)]

        wynik = wynik.to_dict(orient="records")

    return render_template("index.html", wynik=wynik, query=query)

if __name__ == "__main__":
    app.run(debug=True)

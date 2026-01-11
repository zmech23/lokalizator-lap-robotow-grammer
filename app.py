from flask import Flask, render_template, request
import pandas as pd
import re
import os

app = Flask(__name__)

# Wczytanie Excela przy starcie aplikacji
EXCEL_PATH = os.path.join(os.path.dirname(__file__), "data.xlsx")
df = pd.read_excel(EXCEL_PATH)

# Normalizacja kolumny PROJEKT (usuwa spacje, nawiasy itd.)
df["PROJEKT_CLEAN"] = (
    df["PROJEKT"]
    .astype(str)
    .apply(lambda x: re.sub(r'[^A-Za-z0-9]', '', x).lower())
)

@app.route("/", methods=["GET", "POST"])
def index():
    wynik = None
    zapytanie = ""

    if request.method == "POST":
        zapytanie = request.form.get("robot_id", "").strip()

        # Normalizacja tego, co wpisał użytkownik
        szukane = re.sub(r'[^A-Za-z0-9]', '', zapytanie).lower()

        if szukane:
            wynik = df[df["PROJEKT_CLEAN"].str.contains(szukane)]

    return render_template("index.html", wynik=wynik, zapytanie=zapytanie)

if __name__ == "__main__":
    app.run(debug=True)

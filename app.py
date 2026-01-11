from flask import Flask, render_template, request
import pandas as pd
import re
import os

app = Flask(__name__)

# === Wczytanie Excela ===
EXCEL_PATH = os.path.join(os.path.dirname(__file__), "data.xlsx")
df = pd.read_excel(EXCEL_PATH)

# === Funkcja normalizująca ===
def clean(text):
    return re.sub(r'[^a-z0-9]', '', str(text).lower())

# === Normalizacja kolumn ===
df["PROJEKT_CLEAN"] = df["PROJEKT"].apply(clean)
df["MIEJSCE_CLEAN"] = df["MIEJSCE"].apply(clean)
df["SEKCJA_CLEAN"] = df["SEKCJA"].apply(clean)

@app.route("/", methods=["GET", "POST"])
def index():
    wynik = None
    zapytanie = ""

    if request.method == "POST":
        zapytanie = request.form.get("robot_id", "")
        szukane = clean(zapytanie)

        if szukane:
            wynik = df[
                df["PROJEKT_CLEAN"].str.contains(szukane) |
                df["MIEJSCE_CLEAN"].str.contains(szukane) |
                df["SEKCJA_CLEAN"].str.contains(szukane)
            ]

    return render_template("index.html", wynik=wynik, zapytanie=zapytanie)

if __name__ == "__main__":
    app.run(debug=True)


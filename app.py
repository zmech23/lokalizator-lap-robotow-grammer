from flask import Flask, render_template, request
import pandas as pd
import os
import re

app = Flask(__name__)

# ====== ŚCIEŻKA DO PLIKU EXCEL ======
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "data.xlsx")

# ====== WCZYTANIE DANYCH ======
df = pd.read_excel(EXCEL_PATH)

# normalizacja kolumn
df.columns = df.columns.str.strip().str.upper()

# ====== FUNKCJA NORMALIZUJĄCA ======
def normalize(text):
    if pd.isna(text):
        return ""
    text = str(text).upper()
    text = re.sub(r"[()\s]", "", text)  # usuń spacje i nawiasy
    return text

# ====== DODAJ KOLUMNĘ TECHNICZNĄ ======
df["_SEARCH"] = df.apply(
    lambda row: " ".join(normalize(v) for v in row.values),
    axis=1
)

@app.route("/", methods=["GET", "POST"])
def index():
    wynik = None
    query = ""

    if request.method == "POST":
        query = request.form.get("robot_id", "").strip().upper()
        q_norm = normalize(query)

        wynik = df[df["_SEARCH"].str.startswith(q_norm)]

    return render_template("index.html", wynik=wynik, query=query)

if __name__ == "__main__":
    app.run(debug=True)


    return render_template("index.html", wynik=wynik, query=query)

if __name__ == "__main__":
    app.run(debug=True)

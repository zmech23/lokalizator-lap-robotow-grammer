from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# ====== ŚCIEŻKA DO PLIKU EXCEL ======
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "data.xlsx")  # <-- TWOJA NAZWA PLIKU

# ====== WCZYTANIE DANYCH ======
df = pd.read_excel(EXCEL_PATH)

# normalizacja kolumn (żeby uniknąć błędów typu ID / id / spacje)
df.columns = df.columns.str.strip().str.upper()

@app.route("/", methods=["GET", "POST"])
def index():
    wynik = None
    query = ""

    if request.method == "POST":
        query = request.form.get("robot_id", "").strip().upper()

        # wyszukiwanie fragmentu (S11774, wzII, sgm45 itd.)
        mask = df.astype(str).apply(
            lambda col: col.str.upper().str.contains(query, na=False)
        )

        wynik = df[mask.any(axis=1)]

    return render_template("index.html", wynik=wynik, query=query)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "data.xlsx")

df = pd.read_excel(EXCEL_PATH)

@app.route("/", methods=["GET", "POST"])
def index():
    wynik = None

    if request.method == "POST":
        robot_id = request.form.get("robot_id")
        wynik = df[df["ID"] == robot_id]

        if wynik.empty:
            wynik = "Nie znaleziono robota"

    return render_template("index.html", wynik=wynik)

if __name__ == "__main__":
    app.run()

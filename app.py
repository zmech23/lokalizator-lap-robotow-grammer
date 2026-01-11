from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "dane.xlsx")

df = pd.read_excel(EXCEL_PATH)

@app.route("/", methods=["GET", "POST"])
def index():
    wynik = None
    komunikat = None

    if request.method == "POST":
        robot_id = request.form.get("robot_id")

        robot = df[df["PROJEKT"] == robot_id]

        if robot.empty:
            komunikat = f"Nie znaleziono robota o ID: {robot_id}"
        else:
            wynik = robot.to_dict(orient="records")[0]

    return render_template("index.html", wynik=wynik, komunikat=komunikat)

if __name__ == "__main__":
    app.run()

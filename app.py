from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Wczytanie Excela
df = pd.read_excel("dane.xlsx")

@app.route("/", methods=["GET", "POST"])
def index():
    wynik = None
    komunikat = None

    if request.method == "POST":
        robot_id = request.form.get("robot_id")

        # SZUKANIE W KOLUMNIE PROJEKT
        robot = df[df["PROJEKT"] == robot_id]

        if robot.empty:
            komunikat = f"Nie znaleziono robota o ID: {robot_id}"
        else:
            wynik = robot.to_dict(orient="records")[0]

    return render_template("index.html", wynik=wynik, komunikat=komunikat)

if __name__ == "__main__":
    app.run(debug=True)

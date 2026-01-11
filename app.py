from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# wczytanie Excela
df = pd.read_excel("data.xlsx")

# normalizacja kolumny PROJEKT
df["PROJEKT"] = df["PROJEKT"].astype(str).str.strip().str.upper()

@app.route("/", methods=["GET", "POST"])
def index():
    wynik = None

    if request.method == "POST":
        robot_id = request.form.get("robot_id")

        if robot_id:
            robot_id = robot_id.strip().upper()
            wynik = df[df["PROJEKT"] == robot_id]

    return render_template("index.html", wynik=wynik)

if __name__ == "__main__":
    app.run(debug=True)

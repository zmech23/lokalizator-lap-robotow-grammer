from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

df = pd.read_excel("data.xlsx")

@app.route("/", methods=["GET", "POST"])
def index():
    wynik = None

    if request.method == "POST":
        robot_id = request.form.get("robot_id")

        wynik = df[df["PROJEKT"].astype(str).str.contains(robot_id, case=False, na=False)]

    return render_template("index.html", wynik=wynik)

if __name__ == "__main__":
    app.run(debug=True)

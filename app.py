from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

df = pd.read_excel("data.xlsx")
df.columns = df.columns.str.strip()  # usuwa spacje z nagłówków

@app.route("/", methods=["GET", "POST"])
def index():
    wynik = None
    if request.method == "POST":
        robot_id = request.form["robot_id"]

        wynik = df[df["PROJEKT"] == robot_id]

        if wynik.empty:
            wynik = None

    return render_template("index.html", wynik=wynik)

if __name__ == "__main__":
    app.run(debug=True)


    return render_template("index.html", wynik=wynik)

if __name__ == "__main__":
    app.run()

from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Wczytaj Excel
df = pd.read_excel("data.xlsx", dtype=str)
df.columns = ["PROJEKT", "MIEJSCE", "SEKCJA"]
df = df.fillna("")

@app.route("/", methods=["GET", "POST"])
def index():
    query = request.form.get("project_number", "").strip().upper()
    wyniki = []

    if query:
        wyniki = df[df["PROJEKT"].str.upper().str.contains(query)].to_dict(orient="records")

    return render_template(
        "index.html",
        query=query,
        wyniki=wyniki
    )

    )

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Wczytanie danych tylko raz (WAŻNE)
df = pd.read_excel("data/lapy.xlsx")
df = df.fillna("")

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "").strip()
    results = []

    if query:
        q = query.lower()

        mask = (
            df["Projekt"].astype(str).str.lower().str.contains(q)
            | df["Forma"].astype(str).str.lower().str.contains(q)
            | df["Czesc"].astype(str).str.lower().str.contains(q)
        )

        results = df[mask].to_dict(orient="records")

    return render_template(
        "index.html",
        results=results,
        query=query
    )

if __name__ == "__main__":
    app.run(debug=True)


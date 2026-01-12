from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Wczytanie danych
df = pd.read_excel("data.xlsx")
df = df.fillna("")

@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    wynik = []

    if request.method == "POST":
        query = request.form.get("query", "").strip()

        if query:
            query_lower = query.lower()

            mask = df.apply(
                lambda row: row.astype(str).str.lower().str.contains(query_lower).any(),
                axis=1
            )

            wynik = df[mask].to_dict(orient="records")

    return render_template(
        "index.html",
        query=query,
        wynik=wynik
    )

if __name__ == "__main__":
    app.run(debug=True)



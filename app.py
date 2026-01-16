from flask import Flask, render_template, request
import pandas as pd

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# wczytaj Excel tylko raz
df = pd.read_excel("data.xlsx", dtype=str)

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "").strip()
    results = []

    if query:
        mask = df.apply(
            lambda row: row.astype(str).str.contains(query, case=False, na=False).any(),
            axis=1
        )
        results = df[mask].to_dict(orient="records")

    return render_template(
        "index.html",
        results=results,
        query=query
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

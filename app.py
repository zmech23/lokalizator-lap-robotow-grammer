import os
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, "data", "data.xlsx")


df = pd.read_excel(EXCEL_PATH)
df = df.fillna("")

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "").strip()
    results = []

    if query:
        mask = df.astype(str).apply(
            lambda row: row.str.contains(query, case=False, na=False)
        ).any(axis=1)
        results = df[mask].to_dict(orient="records")

    return render_template("index.html", results=results, query=query)

if __name__ == "__main__":
    app.run(debug=True)

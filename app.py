from flask import Flask, render_template, request, send_from_directory
import pandas as pd

app = Flask(
    __name__,
    static_folder="statyczny",
    template_folder="szablony"
)

@app.route("/")
def index():
    query = request.args.get("q", "")
    results = []

    if query:
        df = pd.read_excel("dane.xlsx")
        mask = df.apply(
            lambda row: row.astype(str).str.contains(query, case=False).any(),
            axis=1
        )
        results = df[mask].to_dict(orient="records")

    return render_template("index.html", results=results)

# 🔥 PWA – Service Worker z ROOT
@app.route("/sw.js")
def service_worker():
    return send_from_directory(".", "sw.js", mimetype="application/javascript")

if __name__ == "__main__":
    app.run(debug=True)

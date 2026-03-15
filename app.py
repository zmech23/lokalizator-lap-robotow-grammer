from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Wczytaj dane raz przy starcie
df = pd.read_excel("data.xlsx", dtype=str)
df.columns = ["PROJEKT", "MIEJSCE", "SEKCJA", "MAGAZYN / MASZYNA", "LOKALIZACJA"]
df = df.fillna("")

@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    wyniki = []
    if request.method == "POST":
        query = request.form.get("q", "").strip().upper()
        if query:
            wyniki = df[
                df["PROJEKT"].str.upper().str.contains(query, na=False)
            ].to_dict(orient="records")
    return render_template("index.html", query=query, wyniki=wyniki)

# Endpoint keep-alive — odpowiada na ping z przeglądarki
@app.route("/ping")
def ping():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)

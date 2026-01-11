from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Wczytanie danych z Excela
df = pd.read_excel("data.xlsx")

# Upewniamy się, że kolumna PROJEKT jest tekstem
# ⬇️ ZMIEŃ NA DOKŁADNĄ NAZWĘ KOLUMNY Z EXCELA
KOLUMNA_PROJEKT = "projekt"

df[KOLUMNA_PROJEKT] = df[KOLUMNA_PROJEKT].astype(str)

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "").strip().lower()

    wynik = []

    if query:
        mask = df[KOLUMNA_PROJEKT].str.lower().str.contains(query, na=False)
        wynik = df[mask].to_dict(orient="records")

    return render_template(
        "index.html",
        wynik=wynik,
        query=query
    )

if __name__ == "__main__":
    app.run(debug=True)

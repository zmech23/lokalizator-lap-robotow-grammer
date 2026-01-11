from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# ===== KONFIGURACJA =====
PLIK_EXCEL = "data.xlsx"     # nazwa Twojego pliku
KOLUMNA_PROJEKT = "PROJEKT"  # dokładnie jak w Excelu
# ========================

# Wczytanie danych
df = pd.read_excel(PLIK_EXCEL)

# Ujednolicenie danych (na string + małe litery)
df[KOLUMNA_PROJEKT] = df[KOLUMNA_PROJEKT].astype(str).str.lower()

@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "").strip().lower()
    wynik = []

    if query:
        # SZUKANIE "zawiera"
        wynik = df[df[KOLUMNA_PROJEKT].str.contains(query, na=False)]
        wynik = wynik.to_dict(orient="records")

    return render_template("index.html", wynik=wynik, query=query)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
import pandas as pd
import re

app = Flask(__name__)

# ===== Wczytanie Excela =====
df = pd.read_excel("dane.xlsx")

# ===== Funkcja czyszcząca tekst =====
def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9]", "", text)
    return text

# ===== Czyszczenie wszystkich kolumn =====
for col in df.columns:
    df[col + "_CLEAN"] = df[col].apply(clean_text)

# ===== Główna trasa =====
@app.route("/", methods=["GET", "POST"])
def index():
    wynik = None

    if request.method == "POST":
        query = request.form.get("robot_id", "").lower()

        # Rozbijamy zapytanie na tokeny (np s11777 sgm45)
        tokens = re.findall(r"[a-z0-9]+", query)

        mask = pd.Series([True] * len(df))

        for token in tokens:
            token = clean_text(token)

            token_mask = False
            for col in df.columns:
                if col.endswith("_CLEAN"):
                    token_mask = token_mask | df[col].str.contains(token, na=False)

            mask = mask & token_mask

        wynik = df[mask]

        if wynik.empty:
            wynik = None

    return render_template("index.html", wynik=wynik)


if __name__ == "__main__":
    app.run()

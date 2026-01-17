from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Wczytaj Excel
df = pd.read_excel("data.xlsx", dtype=str)
df = df.fillna("")

# Normalizacja danych
df = df.applymap(lambda x: x.strip().upper())


@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q", "").strip().upper()
    result = None
    error = None

    if query:
        # Zakładamy:
        # kolumna 0 = numer projektu
        # kolumna 1 = lokalizacja
        project_col = df.columns[0]
        location_col = df.columns[1]

        match = df[df[project_col].str.contains(query, na=False)]

        if not match.empty:
            result = match.iloc[0][location_col]
        else:
            error = f"❌ Nie znaleziono projektu: {query}"

    return render_template(
        "index.html",
        result=result,
        error=error,
        query=query
    )


if __name__ == "__main__":
    app.run(debug=True)

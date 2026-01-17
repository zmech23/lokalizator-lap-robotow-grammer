from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Wczytaj dane raz przy starcie aplikacji
df = pd.read_excel("data.xlsx")
df.columns = [col.strip() for col in df.columns]  # czyszczenie nazw kolumn


@app.route("/", methods=["GET"])
def index():
    query = request.args.get("q")
    result = None
    error = None

    if query:
        # szukamy w pierwszej kolumnie
        col_project = df.columns[0]
        col_location = df.columns[1]

        match = df[df[col_project].astype(str) == str(query)]

        if not match.empty:
            result = match.iloc[0][col_location]
        else:
            error = "❌ Nie znaleziono projektu"

    return render_template(
        "index.html",
        result=result,
        error=error,
        query=query
    )


if __name__ == "__main__":
    app.run(debug=True)

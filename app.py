from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd

app = Flask(__name__)
app.secret_key = "lokalizator-grammer-secret"

# Loginy i hasła
USERS = {
    "Wtrysk": "Wtrysk",
    "admin": "WtryskAdmin!"
}

EXCEL_FILE = "LAPY.xlsx"


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]
        if user in USERS and USERS[user] == password:
            session["user"] = user
            return redirect(url_for("search"))
    return render_template("login.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    if "user" not in session:
        return redirect(url_for("login"))

    result = None
    if request.method == "POST":
        project = request.form["project"]
        df = pd.read_excel(EXCEL_FILE)
        found = df[df["Projekt"].astype(str) == project]
        if not found.empty:
            result = found.iloc[0].to_dict()

    return render_template("search.html", result=result)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run()

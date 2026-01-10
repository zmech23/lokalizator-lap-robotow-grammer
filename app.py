from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        robot_id = request.form.get("robot_id")
        return f"Szukanie robota o ID: {robot_id}"
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

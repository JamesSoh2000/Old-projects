from flask import Flask, render_template, request

app = Flask(__name__)

SPORTS = [
    "Soccer",
    "Basketball",
    "Baseball"
]

@app.route("/")

def index():

    return render_template("index.html", sports=SPORTS)

@app.route("/register", methods=["POST"])

def register():
    # This means no value is paseed in to <input name="name"> OR
    if not request.form.get("name") or request.form.get("sport") not in SPORTS:
        return render_template("failure.html")
    else:
        return render_template("success.html")

if __name__ == '__main__':
    app.run()
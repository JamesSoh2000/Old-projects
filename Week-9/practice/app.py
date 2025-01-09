from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")

def index():
    # First
    # name = request.args.get("name") # So I made name variable that takes the key called "name".
    # return render_template("index.html", name=name) # and 왼쪽 name은 key이고 오른쪽이 위에만든 name variable을 key로 사용.

    # My modification
    # name = request.args.get("name_person") # So I made name variable that takes the key called "name_person"
    # return render_template("index.html", name_person=name) # and 왼쪽 name_person은 key이고 오른쪽이 위에만든 name variable을 key로 사용.

    # Second
    return render_template("index.html")

@app.route("/greet", methods=["POST"])

def greet():
    # name = request.args.get("name", "world") # request.args는 GET을 위한 function
    name = request.form.get("name", "world") # request.form은 POST를 위한 function
    return render_template("greet.html", name=name)
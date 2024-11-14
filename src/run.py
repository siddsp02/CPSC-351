# !usr/bin/env python3

from flask import Flask, jsonify, render_template, request

from forms import DFAInputForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "key"  # Will be changed afterwards.


@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    print("Received: ", data)
    return jsonify({"message": "Received data", "data": data}), 200


@app.route("/", methods=["POST", "GET"])
def home():
    form = DFAInputForm()
    
    return render_template("dfa.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)

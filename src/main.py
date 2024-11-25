# !usr/bin/env python3

from flask import Flask, render_template, request, session

from forms import DFAInputForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "key"  # Will be changed afterwards.


@app.route("/", methods=["POST", "GET"])
def home():
    form = DFAInputForm()
    if request.method == "POST":
        data = request.get_json()
        session["data"] = data  # Save DFA data persistently.
        return render_template("graph.html"), 200
    return render_template("dfa.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)

# !usr/bin/env python3

from flask import Flask, render_template

from forms import DFAInputForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "key"  # Will be changed afterwards.


@app.route("/", methods=["POST", "GET"])
def home() -> str:
    form = DFAInputForm()
    return render_template("dfa.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)

# !usr/bin/env python3

from flask import Flask

app = Flask(__name__)


@app.route("/")
def home() -> str:
    return "<h1> Hello world </h1>"


if __name__ == "__main__":
    app.run(debug=True)

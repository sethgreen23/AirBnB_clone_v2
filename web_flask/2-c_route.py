#!/usr/bin/python3
"""
Hello module is a simple module to say hello
"""


from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """ Print Hello HBNB! on the browser """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """ Print HBNB in the browser """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_description(text):
    n_text = text.replace('_', ' ')
    return f'C {n_text}'

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

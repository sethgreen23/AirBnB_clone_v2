#!/usr/bin/python3
"""
Hello module is a simple module to say hello
"""


from flask import Flask


app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_route():
    """ Print Hello HBNB! on the browser """
    return "Hello HBNB!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

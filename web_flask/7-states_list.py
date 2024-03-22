#!/usr/bin/python3
"""
Hello module is a simple module to say hello
"""


from flask import Flask, render_template
from markupsafe import escape
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception=None):
    """ Close session of Database """
    storage.close()


@app.route("/states_list", strict_slashes=False)
def get_states_route():
    """ get the states list """
    return render_template("7-states_list.html", states=storage.all(State))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

#!/usr/bin/env python3
"""i18n compliant flask app"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    """main route"""
    return render_template('0-index.html')


if __name__ == '__main__':
    app.run(debug=True)

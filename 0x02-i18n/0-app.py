#!/usr/bin/env python3
"""i18n compliant flask app"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=True)
def index():
    """main route"""
    return render_template('0-index.html')

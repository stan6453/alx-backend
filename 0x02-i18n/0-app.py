#!/usr/bin/env python3
"""i18n compliant flask app"""

from flask import Flask, render_template
from flask_babel import Babel

app = Flask(__name__)

# Configure available languages


class Config:
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)

# Initialize Babel
babel = Babel(app)


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run()

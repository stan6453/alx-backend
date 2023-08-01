#!/usr/bin/env python3
"""i18n compliant flask app"""

from flask import Flask, render_template
from flask_babel import Babel
from flask import request

app = Flask(__name__)


# Configure available languages
class Config:
    """Config class"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)

# Initialize Babel
babel = Babel(app)


@babel.localeselector
def get_locale():
    """add list of supported languages to flask's Accept-Language header"""
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def index() -> str:
    """main route"""
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run()

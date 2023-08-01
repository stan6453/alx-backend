#!/usr/bin/env python3
"""i18n compliant flask app"""

from flask import Flask, render_template, request, g
from flask_babel import Babel
from flask import request
import pytz
from typing import Mapping, Union


# mock database users
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(id: int) -> Union[Mapping, None]:
    """return a user with the specified id"""
    return users.get(id)


# app starts here
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
def get_locale() -> str:
    """add list of supported languages to flask's Accept-Language header"""
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    locale = g.user and g.user.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    local = request.headers.get('locale')
    if local and local in app.config['LANGUAGES']:
        return local

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    timezone = None
    try:
        timezone = pytz.timezone(request.args.get('timezone'))
        return timezone
    except pytz.UnknownTimeZoneError:
        pass

    try:
        timezone = g.user and pytz.timezone(g.user.get('timezone'))
        if timezone:
            return timezone
    except pytz.UnknownTimeZoneError:
        pass
    
    return pytz.timezone(app.config['BABEL_DEFAULT_TIMEZONE'])


@app.before_request
def before_request():
    """populate flask global variable with the logged-in user"""
    try:
        g.user = get_user(int(request.args.get('login_as')))
    except Exception:
        g.user = None


@app.route('/')
def index() -> str:
    """main route"""
    return render_template('6-index.html')


if __name__ == '__main__':
    app.run()

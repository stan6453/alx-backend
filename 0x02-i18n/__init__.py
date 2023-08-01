#!/usr/bin/env python3
"""init file"""

app = __import__('0-app').app
from flask_babel import Babel
babel = Babel(app)


class Config():
    LANGUAGES = ["en", "fr"]
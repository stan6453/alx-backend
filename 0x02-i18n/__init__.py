#!/usr/bin/env python3
"""init file"""

from flask_babel import Babel
app = __import__('0-app').app
babel = Babel(app)


class Config():
    """config file"""
    LANGUAGES = ["en", "fr"]

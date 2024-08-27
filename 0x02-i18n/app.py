#!/usr/bin/env python3
'''Basic Flask app'''

from flask import Flask, render_template, request, g
from flask_babel import Babel, gettext
import pytz
from pytz.exceptions import UnknownTimeZoneError
from datetime import datetime

# Mock user data
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

# Create a Flask application instance
app = Flask(__name__)

# Initialize Flask-Babel for internationalization
babel = Babel(app)


class Config:
    '''Configuration class for Flask-Babel'''
    LANGUAGES = ["en", "fr"]  # Supported languages
    BABEL_DEFAULT_LOCALE = 'en'  # Default locale if none is specified
    BABEL_DEFAULT_TIMEZONE = 'UTC'  # Default timezone


# Load configuration from the Config class
app.config.from_object(Config)


def get_user():
    '''Retrieve the user from the mock user data based on the login_as
    parameter'''
    user_id = request.args.get('login_as')
    if user_id and user_id.isdigit() and int(user_id) in users:
        return users[int(user_id)]
    return None


@app.before_request
def before_request():
    '''Set the current user in the global context for each request'''
    g.user = get_user()


@babel.localeselector
def get_locale():
    '''Determine the locale to use based on URL
    parameters or accept languages'''
    # Check URL parameters for locale
    lang = request.args.get('locale')
    if lang in app.config['LANGUAGES']:
        return lang
    # Check user settings for locale
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user.get('locale')
    # Use the best match from the Accept-Language header if no URL
    # parameter or user setting is found
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    '''Determine the timezone to use based on URL
    parameters or user settings'''
    # Check URL parameters for timezone
    tz = request.args.get('timezone')
    if tz:
        try:
            return pytz.timezone(tz)
        except UnknownTimeZoneError:
            pass
    # Check user settings for timezone
    if g.user:
        user_tz = g.user.get('timezone')
        if user_tz:
            try:
                return pytz.timezone(user_tz)
            except UnknownTimeZoneError:
                pass
    # Default to UTC if no valid timezone is found
    return pytz.timezone('UTC')


@app.route('/', strict_slashes=False)
def home():
    '''Render the home page template'''
    # Get the current time in the inferred timezone
    tz = get_timezone()
    current_time = datetime.now(tz).strftime('%c')
    return render_template('8-index.html', current_time=current_time)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")

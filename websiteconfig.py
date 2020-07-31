import os
_basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY') or 'deadbeef-foobar-hox'
SENTRY_ENDPOINT = os.environ.get('SENTRY_ENDPOINT') or ''

del os

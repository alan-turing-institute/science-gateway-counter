from config.base import *
# This config is configured for production

DEBUG = False

# Use in-memory SQLlite DB for now
# (will need to update to Azure specific sql/mysql URI
# once Azure webapp + SQL integration is implemented)
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/users.db'

# Disable track modifications as we are not using
# the Flask-SQLAlchemy event system
SQLALCHEMY_TRACK_MODIFICATIONS = False

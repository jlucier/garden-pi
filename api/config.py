import os, sys

# Statement for enabling the development environment
DEBUG = False

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

## Security

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True
# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = 'secret'

# app configuration
DEBUG = True
SECRET_KEY = 'todo-app-secret-key'

SQLALCHEMY_DATABASE_URI = 'sqlite:///appdata.db'

SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# SMTP Settings
SECURITY_EMAIL_SENDER = 'no-reply@example.com'
MAIL_SERVER = 'localhost'
MAIL_PORT = 1025
MAIL_USE_SSL = False
MAIL_USERNAME = ''
MAIL_PASSWORD = ''

# Flask-Security Settings
SECURITY_REGISTERABLE = True
SECURITY_CONFIRMABLE = True
SECURITY_RECOVERABLE = True


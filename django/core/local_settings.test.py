"""
Settings that are specific to this particular instance of the project.
This can contain sensitive information (such as keys) and should not be shared with others.

REMEMBER: If modfiying the content of this file, reflect the changes in local_settings.example.py
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '!km=w2#26v=qbqjw@6$6xut*3&3jlfu&r-r-kns=uo(r1ae)md'

# Create Google RECAPTCHA public and private keys: https://www.google.com/recaptcha/
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''

DEBUG = True

if DEBUG is True:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
else:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

ALLOWED_HOSTS = ['*']

OLD_DATABASE_CONNECTION = "dbname=DBNAME user=USER password=PASS host=HOST port=5432"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'multipal.sqlite3'),
        'TEST': {
            'NAME': os.path.join(BASE_DIR, 'multipal_TEST.sqlite3'),
        },
    }
}

# List of email addresses of users who can view/add/edit/delete select list data in the Admin Dashboard
USERS_CAN_MANAGE_SELECT_LISTS_IN_DASHBOARD = ('...@uni.ac.uk',)

ACCOUNT_CREATE_CODE = 'xxxxx'

TEMP_PASSWORD_FOR_USERS_FROM_OLD_DB = 'xxxxx'

ADMIN_EMAIL = 'ronny.vollandt@lmu.de'

# Email
if DEBUG is True:
    EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')
else:
    EMAIL_USE_TLS = True
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_PORT = '587'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'sender account email address'
    EMAIL_HOST_PASSWORD = 'sender account password'
    DEFAULT_FROM_EMAIL = 'from email address or Project Name (do not reply)'

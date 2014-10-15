import os

UPLOADS_DEFAULT_DEST = "./static/"
DB_URI = os.environ.get("DATABASE_URL", "postgresql://localhost:5432/nahidsamsami")
SECRET_KEY = "this should be a secret"
# Whoosh does not work on Heroku
# WHOOSH_ENABLED = os.environ.get('HEROKU') is None
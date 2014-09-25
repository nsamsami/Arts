import os

UPLOADS_DEFAULT_DEST = "./static/"
DB_URI = os.environ.get("DATABASE_URL", "sqlite:///my_app.db")
SECRET_KEY = "this should be a secret"
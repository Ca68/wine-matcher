import os
from dotenv import load_dotenv

basedir = os.path.dirname(__name__)
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY=os.getenv('SECRET_KEY')
    FLASK_APP=os.getenv('FLASK_APP')
    FLASK_ENV=os.getenv('FLASK_ENV')
    if os.getenv('SQLALCHEMY_DATABASE_URI').startswith('postgres'):
        SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI').replace('postgres', 'postgresql')
    SQLALCHEMY_TRACK_MODIFICATIONS=os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    AWS_ACCESS_KEY_ID=os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY=os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_BUCKET_LOCATION=os.getenv('AWS_BUCKET_LOCATION')
    API_KEY=os.getenv('API_KEY')
    
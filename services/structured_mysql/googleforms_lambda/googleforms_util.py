import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

def create_db_engine():
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASEDIR, '.env'))

    db_host = os.getenv("DATAPLATTFORM_AURORA_HOST")
    db_port = os.getenv("DATAPLATTFORM_AURORA_PORT")
    db_user = os.getenv("DATAPLATTFORM_AURORA_USER")
    db_password = os.getenv("DATAPLATTFORM_AURORA_PASSWORD")
    db_db = os.getenv("DATAPLATTFORM_AURORA_DB_NAME")

    engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_db}?charset=utf8mb4')

    return engine
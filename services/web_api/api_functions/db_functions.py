import pymysql
import os

def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DATAPLATTFORM_AURORA_HOST"),
        port=int(os.getenv("DATAPLATTFORM_AURORA_PORT")),
        user=os.getenv("DATAPLATTFORM_AURORA_USER"),
        password=os.getenv("DATAPLATTFORM_AURORA_PASSWORD"),
        db=os.getenv("DATAPLATTFORM_AURORA_DB_NAME"),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
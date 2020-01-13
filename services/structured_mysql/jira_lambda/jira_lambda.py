from typing import Dict, Union
import json

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import os

'''
from datetime import datetime as dt
from dotenv import load_dotenv

from batch_job_aurora import format_url, fetch_data_url, get_relevant_attrs  # TODO: move code to smaller reusable files
from insert_event_util import get_db_connection
'''


def db():
    db_host = os.getenv("DATAPLATTFORM_AURORA_HOST")
    db_port = os.getenv("DATAPLATTFORM_AURORA_PORT")
    db_user = os.getenv("DATAPLATTFORM_AURORA_USER")
    db_password = os.getenv("DATAPLATTFORM_AURORA_PASSWORD")
    db_db = os.getenv("DATAPLATTFORM_AURORA_DB_NAME")
    engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_db}?charset=utf8mb4')
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    session = Session(engine)

    print("The tables:", Base.metadata.tables.keys())
    print(Base.classes.GithubType)
    '''
    for instance in session.query(Base.classes.JiraSalesType):
        print(instance.issue, instance.customer, instance.issue_status, instance.created, instance.updated)
    '''


def handler(event: Dict, context) -> Dict[str, Union[str, int]]:
    x = json.loads(s=event['Records'][0]['Sns']['Message'])
    print(x['data'])

    return {
        'statusCode': 200,
        'body': 'Done'
    }


from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))

load_dotenv(dotenv_path=os.path.join(BASEDIR, '.env'))

db()

import os
from dotenv import load_dotenv

from sqlalchemy.engine import Engine
from sqlalchemy import MetaData, Table, Column, String, ForeignKey, Sequence, BIGINT, DateTime

import create_engine


def create_tables_if_not_existing(engine: Engine):
    metadata = MetaData()
    metadata.bind = engine

    tablename_jira_issue_created = 'JiraIssueCreated'
    tablename_jira_issue_updated = 'JiraIssueUpdated'
    try:
        if not (engine.has_table(tablename_jira_issue_created) and engine.has_table(tablename_jira_issue_updated)):
            issue_created = Table(
                tablename_jira_issue_created,
                metadata,
                Column('issue', String(32), primary_key=True, nullable=False),
                Column('created', DateTime, nullable=False)
            )
            issue_updated = Table(
                tablename_jira_issue_updated,
                metadata,
                Column(
                    'id',
                    BIGINT(),
                    Sequence('id', start=1, increment=1),
                    primary_key=True
                ),
                Column('issue', String(32), ForeignKey(issue_created.c.issue), nullable=False),
                Column('updated', DateTime, nullable=False),
                Column('issue_status', String(32)),
                Column('customer', String(200))
            )
            metadata.create_all()
    finally:
        engine.dispose()


def main():
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASEDIR, '.env'))
    engine = create_engine.create_db_engine()
    create_tables_if_not_existing(engine)


main()

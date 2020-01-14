from typing import Dict, Union
import json
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

import create_engine

# DB engine is declared outside of the handler in order to be reused between each lambda invocation.
engine = create_engine.create_db_engine()
base = automap_base()
base.prepare(engine, reflect=True)


def insert_jira_data_into_aurora_db(data):
    issue_created_class = base.classes.JiraIssueCreated
    issue_updated_class = base.classes.JiraIssueUpdated
    session = Session(engine)
    try:
        for jira_issue in data:
            existing_issue = session.query(issue_created_class).filter(
                issue_created_class.issue == jira_issue['issue']).first()
            if existing_issue is None:
                session.add(
                    issue_created_class(
                        issue=jira_issue['issue'],
                        created=jira_issue['created']
                    )
                )
            session.add(
                issue_updated_class(
                    issue=jira_issue['issue'],
                    customer=jira_issue['customer'],
                    issue_status=jira_issue['issue_status'],
                    updated=jira_issue['updated']
                )
            )
            session.commit()
    finally:
        session.close()


def handler(event: Dict, context) -> Dict[str, Union[str, int]]:
    message = json.loads(s=event['Records'][0]['Sns']['Message'])
    data = message['data']
    insert_jira_data_into_aurora_db(data=data)

    return {
        'statusCode': 200,
        'body': 'Done'
    }

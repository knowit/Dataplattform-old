import os
from dotenv import load_dotenv
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import json

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASEDIR, '.env'))

db_host = os.getenv("DATAPLATTFORM_AURORA_HOST")
db_port = os.getenv("DATAPLATTFORM_AURORA_PORT")
db_user = os.getenv("DATAPLATTFORM_AURORA_USER")
db_password = os.getenv("DATAPLATTFORM_AURORA_PASSWORD")
db_db = os.getenv("DATAPLATTFORM_AURORA_DB_NAME")

Base = automap_base()
engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_db}?charset=utf8mb4')
Base.prepare(engine, reflect=True)

Form = Base.classes.GoogleFormsType
Question = Base.classes.GoogleFormsQuestionType
Answer = Base.classes.GoogleFormsAnswerType

session = Session(engine)

def handler(event, context):

    sns_message = json.loads(s=event['Records'][0]['Sns']['Message'])
    docs = sns_message['data']

    forms = {}
    questions = []
    answers = []

    records = sorted(docs, key = lambda i: i['responseTimestamp'])

    for record in records:
        forms[record['formId']] = {
            'title': record['formTitle'],
            'description': record['formDescription'] 
            }
        questions.append({
            'unique_id': str(record['questionId'])+str(record['responseTimestamp']),
            'form_id': record['formId'],
            'text_question': record['responseQuestion'],
            'question_type': record['questionType'],
            'form_question_id': record['questionId']
        })
        answers.append({ 
            'unique_question_id': str(record['questionId'])+str(record['responseTimestamp']),
            'response_id': record['responseId'],
            'text_answer': record['responseAnswer'],
            'timestamp': record['responseTimestamp']
        })

    try: 
        for key in list(forms):
            result = session.query(Form).filter(Form.id == key).first()
            if result is None:
                session.add(Form(id=key, title=forms[key]['title'], description=forms[key]['description']))
        for key in range(len(questions)):
            result = session.query(Question).filter(Question.form_question_id == questions[key]['form_question_id'], \
                Question.form_id == questions[key]['form_id']).order_by(Question.version.desc()).first()
            if result is None:
                session.add(Question(unique_id = questions[key]['unique_id'], form_id = questions[key]['form_id'], \
                    text_question=questions[key]['text_question'], type=questions[key]['question_type'], version= 1, form_question_id = questions[key]['form_question_id']))
                session.commit()
                continue
            if (result.text_question != questions[key]['text_question'] or result.type != questions[key]['question_type']):
                questions[key]['version'] = result.version + 1
                session.add(Question(unique_id = questions[key]['unique_id'], form_id = questions[key]['form_id'], text_question=questions[key]['text_question'], \
                    type=questions[key]['question_type'], version=questions[key]['version'], form_question_id = questions[key]['form_question_id']))
                session.commit()
            else:
                for answer in answers:
                    answer.update((k, result.unique_id) for k, v in answer.items() if v == questions[key]['unique_id'])

        for key in range(len(answers)):
            result = session.query(Answer).filter(Answer.unique_question_id == answers[key]['unique_question_id'], \
                Answer.response_id == answers[key]['response_id']).order_by(Answer.version.desc()).first()
            if result is None:
                answers[key]['version'] = 1
                session.add(Answer(unique_question_id = answers[key]['unique_question_id'], response_id = answers[key]['response_id'], \
                    text_answer=answers[key]['text_answer'], timestamp=answers[key]['timestamp'], version=answers[key]['version']))
                session.commit()
                continue
            if result.text_answer != answers[key]['text_answer']:
                answers[key]['version'] = result.version + 1
                session.add(Answer(unique_question_id = answers[key]['unique_question_id'], response_id = answers[key]['response_id'], \
                    text_answer=answers[key]['text_answer'], timestamp=answers[key]['timestamp'], version=answers[key]['version']))
                session.commit()
    finally:
        session.close()

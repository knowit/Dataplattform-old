from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import json
import uuid
from googleforms_util import create_db_engine

# DB engine is declared outside of the handler in order to be reused between each lambda invocation.
engine = create_db_engine()
Base = automap_base()
Base.prepare(engine, reflect=True)

def split_and_sort_records(docs):
    forms = {}
    questions = []
    answers = []
    records = sorted(docs, key = lambda i: i['responseTimestamp'])
    for record in records:
        question_uuid = str(uuid.uuid4())
        answer_uuid = str(uuid.uuid4())
        forms[record['formId']] = {
            'title': record['formTitle'],
            'description': record['formDescription'],
            'created_at': record['formCreated'],
            'owner': record['formOwner'],
            'published_url': record['formPublishedUrl']
            }
        questions.append({
            'unique_id': question_uuid,
            'form_id': record['formId'],
            'text_question': record['responseQuestion'],
            'question_type': record['questionType'],
            'form_question_id': record['questionId']
        })
        answers.append({ 
            'unique_id': answer_uuid,
            'unique_question_id': question_uuid,
            'response_id': record['responseId'],
            'text_answer': record['responseAnswer'],
            'timestamp': record['responseTimestamp'],
            'form_id': record['formId']
        })
    return forms, questions, answers

def insert_or_update_forms_data(forms, questions, answers):
    Form = Base.classes.GoogleFormsType
    Question = Base.classes.GoogleFormsQuestionType
    Answer = Base.classes.GoogleFormsAnswerType
    session = Session(engine)
    try: 
        for key in list(forms):
            result = session.query(Form).filter(Form.id == key).first()
            if result is None:
                session.add(Form(id=key, title=forms[key]['title'], description=forms[key]['description'], created_at=forms[key]['created_at'], \
                    owner=forms[key]['owner'], published_url=forms[key]['published_url']))
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
                session.add(Answer(unique_id = answers[key]['unique_id'], unique_question_id = answers[key]['unique_question_id'], response_id = answers[key]['response_id'], \
                    text_answer=answers[key]['text_answer'], timestamp=answers[key]['timestamp'], version=answers[key]['version'], form_id=answers[key]['form_id']))
                session.commit()
                continue
            if result.text_answer != answers[key]['text_answer']:
                answers[key]['version'] = result.version + 1
                session.add(Answer(unique_id = answers[key]['unique_id'], unique_question_id = answers[key]['unique_question_id'], response_id = answers[key]['response_id'], \
                    text_answer=answers[key]['text_answer'], timestamp=answers[key]['timestamp'], version=answers[key]['version'], form_id=answers[key]['form_id']))
                session.commit()
    finally:
        session.close()
    
def handler(event, context):
    docs = json.loads(s=event['Records'][0]['Sns']['Message'])
    docs = docs['data']

    forms, questions, answers = split_and_sort_records(docs)
    insert_or_update_forms_data(forms,questions,answers)

    return {
            'statusCode': 200,
            'body': 'Done'
    }
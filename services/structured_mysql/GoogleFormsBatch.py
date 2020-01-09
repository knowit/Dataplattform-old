import json
from typing import Dict, Union
import pymysql
import os
from batch_job_aurora.batch_job_aurora import format_url, fetch_data_url
from datetime import datetime as dt
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASEDIR, '.env'))

DEFAULT_TIMESTAMP_TO = timestamp = int(dt.now().timestamp())
DEFAULT_TIMESTAMP_FROM = 1478399468

def main():
    base_url = os.getenv("DATAPLATTFORM_FETCH_URL")
    url = format_url(base_url, 'GoogleFormsType', DEFAULT_TIMESTAMP_FROM, DEFAULT_TIMESTAMP_TO)
    docs = fetch_data_url(url)
    
    connection = pymysql.connect(
    host=os.getenv("DATAPLATTFORM_AURORA_HOST"),
    port=int(os.getenv("DATAPLATTFORM_AURORA_PORT")),
    user=os.getenv("DATAPLATTFORM_AURORA_USER"),
    password=os.getenv("DATAPLATTFORM_AURORA_PASSWORD"),
    db=os.getenv("DATAPLATTFORM_AURORA_DB_NAME"),
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)

    forms = {}
    questions = []
    answers = []

    records = sorted([doc['data'] for doc in docs], key = lambda i: i['responseTimestamp'])

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
        with connection.cursor() as cursor:
            for key in list(forms):
                cursor.execute(f"SELECT id FROM GoogleFormsType WHERE id = '{key}'")
                exists = cursor.fetchone()
                if exists is None:
                    cursor.execute(f"INSERT INTO GoogleFormsType VALUES ('{key}', %s, %s)", (forms[key]['title'], forms[key]['description']))
            for key in range(len(questions)):
                cursor.execute(f"SELECT unique_id, text_question, type, version FROM GoogleFormsQuestionType WHERE form_question_id = '{questions[key]['form_question_id']}' \
                    AND form_id = '{questions[key]['form_id']}' ORDER BY version DESC")
                result = cursor.fetchone()
                if result is None:
                    questions[key]['version'] = 1
                    cursor.execute(f"INSERT INTO GoogleFormsQuestionType VALUES ('{questions[key]['unique_id']}', '{questions[key]['form_id']}', \
                        %s, '{questions[key]['question_type']}', {questions[key]['version']}, {questions[key]['form_question_id']})", (questions[key]['text_question']))
                    connection.commit()
                    continue
                if (result['text_question'] != questions[key]['text_question'] or result['type'] != questions[key]['question_type']):
                    questions[key]['version'] = result['version'] + 1
                    cursor.execute(f"INSERT INTO GoogleFormsQuestionType VALUES ('{questions[key]['unique_id']}', '{questions[key]['form_id']}', \
                        %s, '{questions[key]['question_type']}', {questions[key]['version']}, {questions[key]['form_question_id']})", (questions[key]['text_question']))
                    connection.commit()
                else:
                    for answer in answers:
                        answer.update((k, result['unique_id']) for k, v in answer.items() if v == questions[key]['unique_id'])

            for key in range(len(answers)):
                cursor.execute(f"SELECT text_answer, version FROM GoogleFormsAnswerType WHERE unique_question_id = '{answers[key]['unique_question_id']}' \
                                AND response_id = '{answers[key]['response_id']}' ORDER BY version DESC")
                result = cursor.fetchone()
                if result is None:
                    answers[key]['version'] = 1
                    cursor.execute(f"INSERT INTO GoogleFormsAnswerType VALUES ('{answers[key]['unique_question_id']}', \
                        '{answers[key]['response_id']}', %s, {answers[key]['timestamp']}, {answers[key]['version']})", (answers[key]['text_answer']))
                    connection.commit()
                    continue
                if result['text_answer'] != answers[key]['text_answer']:
                    answers[key]['version'] = result['version'] + 1
                    cursor.execute(f"INSERT INTO GoogleFormsAnswerType VALUES ('{answers[key]['unique_question_id']}', \
                        '{answers[key]['response_id']}', %s, {answers[key]['timestamp']}, {answers[key]['version']})", (answers[key]['text_answer']))
                    connection.commit()
    finally:
        connection.close()

main()
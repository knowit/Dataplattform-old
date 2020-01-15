from googleforms_util import create_db_engine
from sqlalchemy import MetaData, Table, Column, String, ForeignKey, BIGINT, Integer, Text

def create_tables_if_not_existing():
    engine = create_db_engine()
    metadata = MetaData()
    metadata.bind = engine

    tablename_googleforms_forms = 'GoogleFormsType'
    tablename_googleforms_questions = 'GoogleFormsQuestionType'
    tablename_googleforms_answers = 'GoogleFormsAnswerType'
    try:
        if not (engine.has_table(tablename_googleforms_forms) and engine.has_table(tablename_googleforms_questions) and engine.has_table(tablename_googleforms_answers)):
            Table(
                tablename_googleforms_forms,
                metadata,
                Column('id', String(100), primary_key=True, nullable=False),
                Column('title', String(320)),
                Column('description', Text()),
                Column('created_at', BIGINT()),
                Column('owner', String(100)),
                Column('published_url', String(150)),
            )
            Table(
                tablename_googleforms_questions,
                metadata,
                Column('unique_id', String(100), primary_key=True, nullable=False),
                Column('form_question_id', String(100)),
                Column('form_id', String(100)),
                Column('text_question', Text()),
                Column('type', String(100)),
                Column('version', Integer()),
            )
            Table(
                tablename_googleforms_answers,
                metadata,
                Column('unique_id', String(100), primary_key=True, nullable=False),
                Column('unique_question_id', String(100)),
                Column('form_id', String(100)),
                Column('response_id', String(100)),
                Column('text_answer', Text()),
                Column('timestamp', BIGINT()),
                Column('version', Integer()),
            )
            metadata.create_all()
    finally:
        engine.dispose()

def main():
    create_tables_if_not_existing()

main()
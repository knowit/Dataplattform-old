from googleforms_util import create_db_engine
from sqlalchemy import MetaData, Table, Column, String, ForeignKey, BIGINT, Integer, Text, ForeignKey

def create_tables_if_not_existing():
    engine = create_db_engine()
    metadata = MetaData()
    metadata.bind = engine

    tablename_googleforms_forms = 'GoogleFormsType'
    tablename_googleforms_questions = 'GoogleFormsQuestionType'
    tablename_googleforms_answers = 'GoogleFormsAnswerType'
    
    try:
        if not (engine.has_table(tablename_googleforms_forms) 
        and engine.has_table(tablename_googleforms_questions) 
        and engine.has_table(tablename_googleforms_answers)):
            forms = Table(
                tablename_googleforms_forms,
                metadata,
                Column('id', String(100), primary_key=True, nullable=False),
                Column('title', String(320)),
                Column('description', Text()),
                Column('created_at', BIGINT(), nullable=False),
                Column('owner', String(100), nullable=False),
                Column('published_url', String(150), nullable=False),
            )
            questions = Table(
                tablename_googleforms_questions,
                metadata,
                Column('unique_id', String(100), primary_key=True, nullable=False),
                Column('form_question_id', String(100), nullable=False),
                Column('form_id', String(100), ForeignKey(forms.c.id), nullable=False,),
                Column('text_question', Text()),
                Column('type', String(100), nullable=False),
                Column('version', Integer(), nullable=False),
            )
            Table(
                tablename_googleforms_answers,
                metadata,
                Column('unique_id', String(100), primary_key=True, nullable=False),
                Column('unique_question_id', String(100), ForeignKey(questions.c.unique_id), nullable=False),
                Column('form_id', String(100), ForeignKey(forms.c.id), nullable=False),
                Column('response_id', String(100), nullable=False),
                Column('text_answer', Text()),
                Column('timestamp', BIGINT(), nullable=False),
                Column('version', Integer(), nullable=False),
            )
            metadata.create_all()
    finally:
        engine.dispose()

def main():
    create_tables_if_not_existing()

main()
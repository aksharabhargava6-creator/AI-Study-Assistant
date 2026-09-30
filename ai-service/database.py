import psycopg2


def get_connection():

    connection = psycopg2.connect(
        dbname="ai_study_assistant",
        user="aksharabhargava",
        host="localhost",
        port="5432"
    )

    return connection
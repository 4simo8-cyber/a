import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv('DATABASE_URL')
def create_table():
    conn = psycopg2.connect(db_url)
    cursor=conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS product (id SERIAL PRIMARY KEY ,name TEXT  , price TEXT , stock INTEGER , photo BYTEA  ) ''')

    conn.commit()
    conn.close()
if __name__ == "__main__":
    create_table()
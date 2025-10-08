import psycopg2
import os
from dotenv import load_dotenv
from db import db_url

load_dotenv()  # بارگذاری متغیرهای محیطی

def con():
    conn = psycopg2.connect(db_url)
    return conn

def insert(name, price, stock, photo):
    with con() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''INSERT INTO product (name, price, stock, photo) VALUES (%s, %s, %s, %s) ON CONFLICT (name) DO NOTHING''', 
                           (name, price, stock, psycopg2.Binary(photo)))

def select():
    with con() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''SELECT name, price, stock, photo FROM product''')
            return cursor.fetchall()

def update(name, a):
    with con() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''UPDATE product SET stock = %s WHERE name = %s''', (a, name))

def delete(name):
    with con() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''DELETE FROM product WHERE name = %s''', (name,))

def photos(name):
    with con() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''SELECT photo FROM product WHERE name = %s''', (name,))
            return cursor.fetchone()
            

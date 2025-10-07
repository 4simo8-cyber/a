import psycopg2
import os
from dotenv import load_dotenv
from db import db_url



def con():
    conn=psycopg2.connect(db_url)
    cursor=conn.cursor()
    return conn,cursor

def insert(name , price , stock,photo):
    conn,cursor=con()
    cursor.execute('''INSERT OR IGNORE INTO product (name,price,stock,photo) VALUES(%s,%s,%s,%s) ''', (name,price,stock,psycopg2.Binary(photo)) )
    conn.commit()
    conn.close()

def select():
    conn,cursor=con()
    cursor.execute('''SELECT name,price,stock,photo FROM product''')
    datas=cursor.fetchall()
    conn.commit()
    conn.close()
    return datas

def update(name,a):
    conn,cursor=con()
    cursor.execute('''UPDATE product SET stock=%s WHERE name=%s''', (a,name))

    conn.commit()
    conn.close()

def delete(name):
    conn,cursor=con()
    cursor.execute('''DELETE FROM product WHERE name=%s''', (name,))
    conn.commit()
    conn.close()

def photos(name):
    conn,cursor=con()
    cursor.execute('''SELECT photo FROM product WHERE name=%s''',(name,))
    data=cursor.fetchone()
    conn.commit()
    conn.close()
    return data
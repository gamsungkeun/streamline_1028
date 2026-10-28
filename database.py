import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "mycom.db"

def get_db_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    '''초기 테이블 생성 함수'''
    conn = get_db_connection()
    c = conn.cursor()
    # 사용자 테이블 생성
    c.execute('''
    CREATE TABLE IF NOT EXISTS user_table (
        id_num INTEGER PRIMARY KEY AUTOINCREMENT,
        userid TEXT NOT NULL UNIQUE COLLATE NOCASE,
        username TEXT NOT NULL, 
        password TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE COLLATE NOCASE,
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    # 설문 테이블 생성
    c.execute('''
    CREATE TABLE IF NOT EXISTS survey_table (
        id_num INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        q1 INTEGER, q2 INTEGER, q3 INTEGER, q4 INTEGER, q5 INTEGER,
        q6 INTEGER, q7 INTEGER, q8 INTEGER, q9 INTEGER, q10 INTEGER,
        created_at TEXT
    )
    ''')
    conn.commit()
    conn.close()

def create_user(userid, username, password, email):
    '''사용자 생성 함수'''
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO user_table (userid, username, password, email) VALUES (?, ?, ?, ?)",
                  (userid, username, password, email))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(userid, password):
    '''사용자 로그인 함수'''
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM user_table WHERE userid=? AND password=?", (userid, password))
    data = c.fetchall()
    conn.close()
    return data

def insert_survey_data(user_id, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10):
    '''설문 응답을 DB에 저장하는 함수'''
    conn = get_db_connection()
    c = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    query = """
    INSERT INTO survey_table (user_id, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    c.execute(query, (user_id, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, created_at))
    conn.commit()
    conn.close()

def fetch_survey_data():
    '''설문 결과를 Pandas DataFrame으로 불러오는 함수'''
    conn = get_db_connection()
    query = "SELECT * FROM survey_table"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

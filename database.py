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
    # 학습 이력 테이블 생성 (메뉴 클릭 기록 + 체류 시간(초))
    c.execute('''
    CREATE TABLE IF NOT EXISTS learning_history (
        id_num INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        menu_id TEXT NOT NULL,
        waiting_time INTEGER DEFAULT 0,
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

def insert_learning_history(user_id, menu_id):
    '''메뉴 클릭 시 학습 이력을 저장하고, 생성된 행의 id를 반환하는 함수'''
    conn = get_db_connection()
    c = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO learning_history (user_id, menu_id, waiting_time, created_at) VALUES (?, ?, 0, ?)",
              (user_id, menu_id, created_at))
    conn.commit()
    row_id = c.lastrowid
    conn.close()
    return row_id

def update_waiting_time(row_id, waiting_time):
    '''다른 메뉴로 이동할 때, 이전 메뉴의 체류 시간(초)을 저장하는 함수'''
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE learning_history SET waiting_time=? WHERE id_num=?", (waiting_time, row_id))
    conn.commit()
    conn.close()

def fetch_menu_order(user_id, menus):
    '''학습 이력을 참조하여 총 체류 시간(같으면 클릭 수)이 많은 순으로 메뉴를 정렬하는 함수'''
    conn = get_db_connection()
    query = """
    SELECT menu_id, SUM(waiting_time) AS total_time, COUNT(*) AS clicks
    FROM learning_history WHERE user_id=? GROUP BY menu_id
    """
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    stats = {r.menu_id: (r.total_time, r.clicks) for r in df.itertuples()}
    return sorted(menus, key=lambda m: stats.get(m, (0, 0)), reverse=True)

def fetch_learning_history(user_id):
    '''사용자의 학습 이력을 Pandas DataFrame으로 불러오는 함수'''
    conn = get_db_connection()
    query = "SELECT * FROM learning_history WHERE user_id=? ORDER BY id_num DESC"
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    return df

import sqlite3


def login(user_id, password):
    # 대놓고 SQL Injection이 발생하는 코드
    db = sqlite3.connect("users.db")
    cursor = db.cursor()
    
    query = f"SELECT * FROM users WHERE id = '{user_id}' AND pw = '{password}'"
    cursor.execute(query)
    return cursor.fetchone()

# 보안 점검 테스트용


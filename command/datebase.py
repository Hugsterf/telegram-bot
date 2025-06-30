import sqlite3
import time

conn = sqlite3.connect('casino.db')
cursor = conn.cursor()

print("Начинаю создавать таблицу users...")
try:
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        balance INTEGER DEFAULT 0,
        balance_on_bank INTEGER DEFAULT 1000,
        last_work_time REAL DEFAULT 0,
        last_crime_time REAL DEFAULT 0,
        last_riskwork_time REAL DEFAULT 0,
        last_collect_time REAL DEFAULT 0,
        last_rob_time REAL DEFAULT 0,
        job TEXT DEFAULT 'NO_JOB',
        job_type TEXT DEFAULT 'NO_JOB_Type',
        hard_level_skils INTEGER DEFAULT 0,
        soft_level_skils INTEGER DEFAULT 0,
        salary_hard_soft INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    print("Таблица users успешно создана.")
except Exception as e:
    print(f"Ошибка при создании таблицы: {e}")


def get_balance(user_id):
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute(
            "INSERT INTO users (user_id, balance) VALUES (?, ?)", 
            (user_id, 0)
        )
        conn.commit()
        return 0 
    
def get_username(user_id):
    cursor.execute("SELECT username FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
            return result[0]
    else:
            return None


def update_balance(user_id, new_balance):
    cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id))
    conn.commit()

def get_balance_on_bank(user_id):
    cursor.execute("SELECT balance_on_bank FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        cursor.execute(
            "INSERT INTO users (user_id, balance_on_bank) VALUES (?, ?)", 
            (user_id, 1000) 
        )
        conn.commit()
        return 1000

def update_balance_on_bank(user_id, new_balance_on_bank):
    cursor.execute("UPDATE users SET balance_on_bank = ? WHERE user_id = ?", (new_balance_on_bank, user_id))
    conn.commit()

#lvl
def get_hard_level_user(user_id):
    cursor.execute("SELECT hard_level_skils FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return 0


def update_username(user_id, newname):
    cursor.execute("UPDATE users SET username = ? WHERE user_id = ?", (newname, user_id))
    conn.commit()


def update_hard_level_user(user_id, new_lvl):
    cursor.execute("UPDATE users SET hard_level_skils = ? WHERE user_id = ?", (new_lvl, user_id))
    conn.commit()


def get_soft_level_user(user_id):
    cursor.execute("SELECT soft_level_skils FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return 0


def update_soft_level_user(user_id, new_lvl):
    cursor.execute("UPDATE users SET soft_level_skils = ? WHERE user_id = ?", (new_lvl, user_id))
    conn.commit()
#lvl

def get_salary_skills_user(user_id):
    cursor.execute("SELECT salary_hard_soft FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return 0


def update_salary_skill_user(user_id, new_salary):
    cursor.execute("UPDATE users SET salary_hard_soft = ? WHERE user_id = ?", (new_salary, user_id))
    conn.commit()


def update_last_work_time(user_id):
    cursor.execute("UPDATE users SET last_work_time = ? WHERE user_id = ?", (time.time(), user_id))
    conn.commit()

def get_last_rob_time(user_id):
        cursor.execute("SELECT last_rob_time FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        return result[0] if result else 0
    
def update_last_rob_time(user_id: int, timestamp: float):
    try:
        cursor.execute(
            "UPDATE users SET last_rob_time = ? WHERE user_id = ?",
            (timestamp, user_id)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"❌ Ошибка при обновлении времени ограбления: {e}")
        conn.rollback()
        return False

def get_last_work_time(user_id):
    cursor.execute("SELECT last_work_time FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return 0
    
def update_last_crime_time(user_id):
    cursor.execute("UPDATE users SET last_crime_time = ? WHERE user_id = ?", (time.time(), user_id))
    conn.commit()

def get_last_crime_time(user_id):
    cursor.execute("SELECT last_crime_time FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return 0
    
def get_user_job(user_id):
    cursor.execute("SELECT job FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return None
    
def update_job(user_id, new_job):
    cursor.execute("UPDATE users SET job = ? WHERE user_id = ?", (new_job, user_id))
    conn.commit()

def update_job_type(user_id, new_job_type):
    cursor.execute("UPDATE users SET job_type = ? WHERE user_id = ?", (new_job_type, user_id))
    conn.commit()

def get_job_type(user_id):
    cursor.execute("SELECT job_type FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return 0

def get_change_job_time(user_id):
    cursor.execute("SELECT change_job_time FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return 0

def update_change_job_time(user_id):
    cursor.execute("UPDATE users SET change_job_time = ? WHERE user_id = ?", (time.time(), user_id))
    conn.commit()

def update_last_riskwork_time(user_id):
    cursor.execute("UPDATE users SET last_riskwork_time = ? WHERE user_id = ?", (time.time(), user_id))
    conn.commit()

def get_last_riskwork_time(user_id):
    cursor.execute("SELECT last_riskwork_time FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return 0
    
def get_last_collect_time(user_id):
    cursor.execute("SELECT last_collect_time FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return 0
    
def update_last_collect_time(user_id):
    cursor.execute("UPDATE users SET last_collect_time = ? WHERE user_id = ?", (time.time(), user_id))
    conn.commit()
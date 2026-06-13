import sqlite3
from pathlib import Path
from datetime import datetime, date

DB_PATH = Path("data") / "goalbot.db"


def connect():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            created_at TEXT NOT NULL,

            goal TEXT,
            target_amount REAL,
            current_amount REAL DEFAULT 0,
            months INTEGER,

            has_job INTEGER DEFAULT 0,
            preferred_job TEXT,
            city TEXT,

            streak INTEGER DEFAULT 0,
            best_streak INTEGER DEFAULT 0,
            total_steps INTEGER DEFAULT 0,
            last_checkin_date TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT,
            note TEXT,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS job_searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            job_type TEXT NOT NULL,
            city TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS job_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            job_type TEXT,
            city TEXT,
            created_at TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reminder_settings (
            user_id INTEGER PRIMARY KEY,
            enabled INTEGER DEFAULT 1,
            hour INTEGER DEFAULT 22,
            minute INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


def create_user(user_id: int, username: str | None, first_name: str | None):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO users (user_id, username, first_name, created_at)
        VALUES (?, ?, ?, ?)
    """, (user_id, username, first_name, datetime.now().isoformat()))

    cur.execute("""
        INSERT OR IGNORE INTO reminder_settings (user_id, enabled, hour, minute)
        VALUES (?, 1, 22, 0)
    """, (user_id,))

    conn.commit()
    conn.close()


def get_user(user_id: int):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row


def get_all_users_with_reminders():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.user_id, u.goal, u.streak, r.enabled, r.hour, r.minute
        FROM users u
        JOIN reminder_settings r ON r.user_id = u.user_id
        WHERE r.enabled = 1
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def set_reminder(user_id: int, enabled: int = 1, hour: int = 22, minute: int = 0):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO reminder_settings (user_id, enabled, hour, minute)
        VALUES (?, ?, ?, ?)
    """, (user_id, enabled, hour, minute))
    conn.commit()
    conn.close()


def save_goal(user_id: int, goal: str, target_amount: float, current_amount: float, months: int):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET goal = ?, target_amount = ?, current_amount = ?, months = ?
        WHERE user_id = ?
    """, (goal, target_amount, current_amount, months, user_id))
    conn.commit()
    conn.close()


def delete_goal(user_id: int):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET goal = NULL, target_amount = NULL, current_amount = 0, months = NULL
        WHERE user_id = ?
    """, (user_id,))
    conn.commit()
    conn.close()


def set_has_job(user_id: int, has_job: int):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET has_job = ? WHERE user_id = ?", (has_job, user_id))
    conn.commit()
    conn.close()


def save_job_preference(user_id: int, job_type: str, city: str):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET preferred_job = ?, city = ?
        WHERE user_id = ?
    """, (job_type, city, user_id))

    cur.execute("""
        INSERT INTO job_searches (user_id, job_type, city, created_at)
        VALUES (?, ?, ?, ?)
    """, (user_id, job_type, city, datetime.now().isoformat()))

    conn.commit()
    conn.close()


def add_job_application(user_id: int):
    user = get_user(user_id)
    job_type = user["preferred_job"] if user else None
    city = user["city"] if user else None

    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO job_applications (user_id, job_type, city, created_at)
        VALUES (?, ?, ?, ?)
    """, (user_id, job_type, city, datetime.now().isoformat()))
    conn.commit()
    conn.close()


def count_job_applications(user_id: int):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS c FROM job_applications WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return int(row["c"] or 0)


def update_current_amount(user_id: int, current_amount: float):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET current_amount = ? WHERE user_id = ?", (current_amount, user_id))
    conn.commit()
    conn.close()


def add_transaction(user_id: int, tx_type: str, amount: float, category: str, note: str):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO transactions (user_id, type, amount, category, note, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, tx_type, amount, category, note, datetime.now().isoformat()))

    user = get_user(user_id)
    current = float(user["current_amount"] or 0) if user else 0

    if tx_type == "income":
        current += amount
    elif tx_type == "expense":
        current = max(current - amount, 0)

    cur.execute("UPDATE users SET current_amount = ? WHERE user_id = ?", (current, user_id))

    conn.commit()
    conn.close()


def get_summary(user_id: int, period: str | None = None):
    where = "WHERE user_id = ?"
    params = [user_id]

    if period == "week":
        where += " AND datetime(created_at) >= datetime('now', '-7 days')"
    elif period == "month":
        where += " AND datetime(created_at) >= datetime('now', '-30 days')"

    conn = connect()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT
            COALESCE(SUM(CASE WHEN type='income' THEN amount ELSE 0 END), 0) AS income,
            COALESCE(SUM(CASE WHEN type='expense' THEN amount ELSE 0 END), 0) AS expense
        FROM transactions
        {where}
    """, params)
    row = cur.fetchone()
    conn.close()
    return row


def get_expenses_by_category(user_id: int, period: str | None = None):
    where = "WHERE user_id = ? AND type = 'expense'"
    params = [user_id]

    if period == "week":
        where += " AND datetime(created_at) >= datetime('now', '-7 days')"
    elif period == "month":
        where += " AND datetime(created_at) >= datetime('now', '-30 days')"

    conn = connect()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT category, SUM(amount) AS total
        FROM transactions
        {where}
        GROUP BY category
        ORDER BY total DESC
    """, params)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_recent_transactions(user_id: int, limit: int = 5):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM transactions
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (user_id, limit))
    rows = cur.fetchall()
    conn.close()
    return rows


def mark_step_done(user_id: int):
    user = get_user(user_id)
    today = date.today().isoformat()

    streak = int(user["streak"] or 0)
    best = int(user["best_streak"] or 0)
    total_steps = int(user["total_steps"] or 0)
    last_date = user["last_checkin_date"]

    if last_date != today:
        streak += 1
        total_steps += 1
        best = max(best, streak)

    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET streak = ?, best_streak = ?, total_steps = ?, last_checkin_date = ?
        WHERE user_id = ?
    """, (streak, best, total_steps, today, user_id))
    conn.commit()
    conn.close()

    return streak, best, total_steps


def mark_failed(user_id: int):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET streak = 0, last_checkin_date = ?
        WHERE user_id = ?
    """, (date.today().isoformat(), user_id))
    conn.commit()
    conn.close()

import os
import sqlite3
from typing import Optional, Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "aria.db")


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        # Adiciona colunas de segurança se não existirem
        try:
            cur.execute("ALTER TABLE users ADD COLUMN failed_attempts INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass
        try:
            cur.execute("ALTER TABLE users ADD COLUMN locked_until DATETIME")
        except sqlite3.OperationalError:
            pass
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                name TEXT DEFAULT 'Aventureiro',
                strength INTEGER DEFAULT 5,
                intelligence INTEGER DEFAULT 5,
                agility INTEGER DEFAULT 5,
                hair_color TEXT DEFAULT 'Castanho',
                hair_style TEXT DEFAULT 'Curto',
                skin_tone TEXT DEFAULT 'Clara',
                eye_color TEXT DEFAULT 'Castanho',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
            """
        )
        conn.commit()


def get_user_by_username(username: str) -> Optional[sqlite3.Row]:
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cur.fetchone()


def create_user(username: str, password_hash: str) -> int:
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash),
        )
        conn.commit()
        return int(cur.lastrowid)


def get_character_by_user(user_id: int) -> Optional[sqlite3.Row]:
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM characters WHERE user_id = ?", (user_id,))
        return cur.fetchone()


def upsert_character(user_id: int, data: Dict[str, Any]) -> None:
    fields = [
        "name",
        "strength",
        "intelligence",
        "agility",
        "hair_color",
        "hair_style",
        "skin_tone",
        "eye_color",
    ]
    values = [data.get(f) for f in fields]

    with _connect() as conn:
        cur = conn.cursor()
        existing = get_character_by_user(user_id)
        if existing:
            set_clause = ", ".join(f"{f} = ?" for f in fields)
            cur.execute(
                f"UPDATE characters SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?",
                (*values, user_id),
            )
        else:
            placeholders = ", ".join("?" for _ in fields)
            cur.execute(
                f"INSERT INTO characters (user_id, {', '.join(fields)}) VALUES (?, {placeholders})",
                (user_id, *values),
            )
        conn.commit()


def register_failed_login(user_id: int, threshold: int, lock_minutes: int) -> None:
    """Incrementa falhas e aplica bloqueio temporário ao atingir o limite."""
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE users SET failed_attempts = COALESCE(failed_attempts,0) + 1 WHERE id = ?", (user_id,))
        cur.execute("SELECT failed_attempts FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        attempts = int(row[0]) if row else 0
        if attempts >= threshold:
            cur.execute(
                "UPDATE users SET locked_until = DATETIME('now', ?), failed_attempts = 0 WHERE id = ?",
                (f"+{int(lock_minutes)} minutes", user_id),
            )
        conn.commit()


def reset_failed_login(user_id: int) -> None:
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE users SET failed_attempts = 0, locked_until = NULL WHERE id = ?", (user_id,))
        conn.commit()


def get_lock_remaining_minutes(user_id: int) -> int:
    """Retorna minutos restantes de bloqueio (>0) ou 0 se não bloqueado."""
    with _connect() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
              CASE
                WHEN locked_until IS NULL THEN 0
                WHEN locked_until > CURRENT_TIMESTAMP THEN CAST((JULIANDAY(locked_until) - JULIANDAY(CURRENT_TIMESTAMP))*24*60 AS INTEGER) + 1
                ELSE 0
              END AS remaining
            FROM users WHERE id = ?
            """,
            (user_id,),
        )
        row = cur.fetchone()
        return int(row[0]) if row and row[0] is not None else 0

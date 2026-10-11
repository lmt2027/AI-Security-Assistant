
import sqlite3
from datetime import datetime

DATABASE_NAME = "security_assistant.db"



def create_database():
    with sqlite3.connect(DATABASE_NAME) as connection:

        # Table for reviewed security alerts
        connection.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                alert_id TEXT PRIMARY KEY,
                alert_name TEXT NOT NULL,
                reviewed_at TEXT NOT NULL
            )
        """)

        # Table for automatically detected warnings
        connection.execute("""
            CREATE TABLE IF NOT EXISTS detected_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                severity TEXT NOT NULL,
                explanation TEXT NOT NULL,
                recommendation TEXT NOT NULL,
                failed_attempts INTEGER NOT NULL,
                detected_at TEXT NOT NULL
            )
        """)



def save_review(alert_id, alert_name):
    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.execute(
            """
            INSERT OR IGNORE INTO reviews
            (alert_id, alert_name, reviewed_at)
            VALUES (?, ?, ?)
            """,
            (
                alert_id,
                alert_name,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )


def get_reviews():
    with sqlite3.connect(DATABASE_NAME) as connection:
        cursor = connection.execute(
            """
            SELECT alert_id, alert_name, reviewed_at
            FROM reviews
            ORDER BY reviewed_at DESC
            """
        )
        return cursor.fetchall()



def save_detected_alert(alert):
    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.execute(
            """
            INSERT INTO detected_alerts (
                title,
                severity,
                explanation,
                recommendation,
                failed_attempts,
                detected_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                alert["title"],
                alert["severity"],
                alert["explanation"],
                alert["recommendation"],
                alert["failed_attempts"],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )



def get_detected_alerts():
    with sqlite3.connect(DATABASE_NAME) as connection:
        cursor = connection.execute(
            """
            SELECT
                id,
                title,
                severity,
                explanation,
                recommendation,
                failed_attempts,
                detected_at
            FROM detected_alerts
            ORDER BY id DESC
            """
        )
        return cursor.fetchall()

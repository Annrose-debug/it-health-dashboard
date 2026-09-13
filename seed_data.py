import sqlite3
from datetime import datetime, timedelta

DB_NAME = "it_dashboard.db"

def seed_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Drop old tables so we can recreate them with the correct columns
    cursor.execute('DROP TABLE IF EXISTS system_logs')
    cursor.execute('DROP TABLE IF EXISTS security_alerts')
    cursor.execute('DROP TABLE IF EXISTS support_tickets')

    # Recreate tables matching frontend/API expectations
    cursor.execute('''
        CREATE TABLE system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            endpoint TEXT,
            status_code INTEGER,
            latency REAL,
            timestamp TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE security_alerts (
            alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            attempts INTEGER,
            timestamp TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE support_tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            error_message TEXT,
            status TEXT,
            timestamp TEXT
        )
    ''')

    # Insert realistic system logs
    now = datetime.now()
    logs_data = [
        ("/api/v1/auth/login", 200, 0.142, (now - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")),
        ("/api/v1/vault/sync", 500, 1.890, (now - timedelta(minutes=4)).strftime("%Y-%m-%d %H:%M:%S")),
        ("/healthz", 200, 0.031, (now - timedelta(minutes=3)).strftime("%Y-%m-%d %H:%M:%S")),
        ("/api/v1/payments/process", 403, 0.412, (now - timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M:%S")),
        ("/api/v1/users/profile", 200, 0.089, (now - timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S")),
        ("/api/v1/admin/config", 502, 2.450, now.strftime("%Y-%m-%d %H:%M:%S")),
    ]
    cursor.executemany('INSERT INTO system_logs (endpoint, status_code, latency, timestamp) VALUES (?, ?, ?, ?)', logs_data)

    # Insert realistic security alerts
    security_data = [
        ("192.168.1.104", 14, now.strftime("%Y-%m-%d %H:%M:%S")),
        ("45.33.21.189", 32, (now - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")),
        ("10.0.0.45", 8, (now - timedelta(minutes=25)).strftime("%Y-%m-%d %H:%M:%S")),
    ]
    cursor.executemany('INSERT INTO security_alerts (ip, attempts, timestamp) VALUES (?, ?, ?)', security_data)

    # Insert realistic support tickets
    tickets_data = [
        ("Database connection pool exhausted on /vault/sync", "OPEN", now.strftime("%Y-%m-%d %H:%M:%S")),
        ("Gateway timeout (502) on /admin/config endpoint", "OPEN", (now - timedelta(minutes=6)).strftime("%Y-%m-%d %H:%M:%S")),
    ]
    cursor.executemany('INSERT INTO support_tickets (error_message, status, timestamp) VALUES (?, ?, ?)', tickets_data)

    conn.commit()
    conn.close()
    print("Database freshly dropped, recreated, and seeded with high-fidelity telemetry data!")

if __name__ == '__main__':
    seed_database()
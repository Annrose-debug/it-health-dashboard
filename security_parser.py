import sqlite3
from collections import defaultdict
from datetime import datetime

LOG_FILE = "server_access.log"
DB_NAME = "it_dashboard.db"
FAILED_THRESHOLD = 5

def init_security_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS security_alerts (
            alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            failed_attempts INTEGER,
            alert_level TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def parse_security_logs():
    failed_counts = defaultdict(int)
    
    print(f"\n--- Scanning Server Logs [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ---")
    
    try:
        with open(LOG_FILE, "r") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) >= 4:
                    ip = parts[2]
                    action = parts[3]
                    if action == "LOGIN_FAILED":
                        failed_counts[ip] += 1

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        for ip, count in failed_counts.items():
            if count >= FAILED_THRESHOLD:
                print(f"  [SECURITY ALERT] Suspicious Activity Detected!")
                print(f"  IP: {ip} | Failed Attempts: {count} | Status: FLAG_BRUTE_FORCE")
                
                # Check if alert already logged
                cursor.execute("SELECT alert_id FROM security_alerts WHERE ip_address = ?", (ip,))
                if not cursor.fetchone():
                    cursor.execute('''
                        INSERT INTO security_alerts (ip_address, failed_attempts, alert_level)
                        VALUES (?, ?, ?)
                    ''', (ip, count, "CRITICAL"))
            else:
                print(f"  [LOG AUDIT] IP: {ip} | Failed Attempts: {count} (Normal)")

        conn.commit()
        conn.close()

    except FileNotFoundError:
        print(f"Error: Log file '{LOG_FILE}' not found.")

if __name__ == "__main__":
    init_security_table()
    parse_security_logs()
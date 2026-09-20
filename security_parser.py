import time
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
            ip TEXT,
            attempts INTEGER,
            alert_level TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Safely ensure the alert_level column exists even if table was pre-created
    try:
        cursor.execute("ALTER TABLE security_alerts ADD COLUMN alert_level TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists, safe to ignore

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
                
                # Check if alert already logged for this IP
                cursor.execute("SELECT alert_id FROM security_alerts WHERE ip = ?", (ip,))
                existing = cursor.fetchone()
                
                if not existing:
                    cursor.execute('''
                        INSERT INTO security_alerts (ip, attempts, alert_level)
                        VALUES (?, ?, ?)
                    ''', (ip, count, "CRITICAL"))
                else:
                    # Update attempts if it's already in the table
                    cursor.execute('''
                        UPDATE security_alerts 
                        SET attempts = ?, timestamp = CURRENT_TIMESTAMP 
                        WHERE ip = ?
                    ''', (count, ip))
            else:
                print(f"  [LOG AUDIT] IP: {ip} | Failed Attempts: {count} (Normal)")

        conn.commit()
        conn.close()

    except FileNotFoundError:
        print(f"Error: Log file '{LOG_FILE}' not found. Creating a blank one for simulation...")
        with open(LOG_FILE, "w") as f:
            f.write("2026-09-16 19:00:00 192.168.1.50 LOGIN_FAILED\n")

if __name__ == "__main__":
    init_security_table()
    print("Starting Security Log Parser & Threat Engine. Press Ctrl+C to stop.")
    try:
        while True:
            parse_security_logs()
            time.sleep(15)  # Scan logs every 15 seconds
    except KeyboardInterrupt:
        print("\nSecurity monitoring engine stopped gracefully.")
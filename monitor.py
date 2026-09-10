import time
import sqlite3
import requests
from datetime import datetime

# 1. Configuration & Target Endpoints
TARGETS = [
    {"name": "Google Main", "url": "https://www.google.com"},
    {"name": "GitHub API", "url": "https://api.github.com"},
    {"name": "Broken Endpoint Test", "url": "https://httpbin.org/status/500"},
]

DB_NAME = "it_dashboard.db"

# 2. Database Setup (system_logs & support_tickets)
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Table 1: System Check Logs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT,
            url TEXT,
            status_code INTEGER,
            response_time_ms REAL,
            status_label TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table 2: Auto-Generated Support Tickets
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS support_tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT,
            issue_description TEXT,
            severity TEXT,
            status TEXT DEFAULT 'OPEN',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# 3. Ticket Escalation Logic
def create_support_ticket(cursor, service_name, status_code, status_label):
    # Check if an OPEN ticket already exists for this service to prevent spamming
    cursor.execute('''
        SELECT ticket_id FROM support_tickets 
        WHERE service_name = ? AND status = 'OPEN'
    ''', (service_name,))
    
    existing_ticket = cursor.fetchone()
    
    if not existing_ticket:
        severity = "HIGH" if status_label == "CRITICAL_DOWN" else "MEDIUM"
        issue_desc = f"Service returned status code {status_code} ({status_label})."
        
        cursor.execute('''
            INSERT INTO support_tickets (service_name, issue_description, severity)
            VALUES (?, ?, ?)
        ''', (service_name, issue_desc, severity))
        
        print(f"  [AUTO-TICKET CREATED] Ticket logged for {service_name} | Severity: {severity}")

# 4. Health Check Engine
def check_services():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print(f"\n--- Running Health Check [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ---")

    for target in TARGETS:
        name = target["name"]
        url = target["url"]
        
        try:
            start_time = time.time()
            response = requests.get(url, timeout=5)
            latency = round((time.time() - start_time) * 1000, 2)
            status_code = response.status_code

            if status_code == 200:
                status_label = "HEALTHY"
            else:
                status_label = "WARNING/ERROR"

        except requests.exceptions.RequestException:
            status_code = 0
            latency = 0.0
            status_label = "CRITICAL_DOWN"

        # Log system metrics
        cursor.execute('''
            INSERT INTO system_logs (service_name, url, status_code, response_time_ms, status_label)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, url, status_code, latency, status_label))

        print(f"[{status_label}] {name} | Code: {status_code} | Latency: {latency}ms")

        # Trigger auto-escalation if service is not healthy
        if status_label != "HEALTHY":
            create_support_ticket(cursor, name, status_code, status_label)

    conn.commit()
    conn.close()

# 5. Main Execution Loop
if __name__ == "__main__":
    init_db()
    print("Starting IT Health & Escalation Engine. Press Ctrl+C to stop.")
    try:
        while True:
            check_services()
            time.sleep(10)
    except KeyboardInterrupt:
        print("\nMonitoring engine stopped gracefully.")
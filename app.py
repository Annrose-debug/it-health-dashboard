import sqlite3
from flask import Flask, jsonify, render_template

app = Flask(__name__)
DB_NAME = "it_dashboard.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Returns rows as dictionary-like objects
    return conn

# Index Page
@app.route('/')
def index():
    return render_template('index.html')

# 1. Health Status Logs Endpoint (Mapped to new worker schema)
@app.route('/api/logs', methods=['GET'])
def get_logs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM system_logs ORDER BY id DESC LIMIT 20')
    rows = cursor.fetchall()
    conn.close()
    
    logs = []
    for row in rows:
        logs.append({
            "id": row["id"],
            "service_name": row["service_name"],
            "url": row["url"],
            "status_code": row["status_code"],
            "response_time_ms": row["response_time_ms"],
            "status_label": row["status_label"],
            "timestamp": row["timestamp"]
        })
    return jsonify(logs)

# 2. Support Tickets Endpoint
@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM support_tickets ORDER BY ticket_id DESC')
    rows = cursor.fetchall()
    conn.close()
    
    tickets = []
    for row in rows:
        tickets.append({
            "ticket_id": row["ticket_id"],
            "service_name": row["service_name"],
            "issue_description": row["issue_description"],
            "severity": row["severity"],
            "status": row["status"],
            "created_at": row["created_at"]
        })
    return jsonify(tickets)

# 3. Security Alerts Endpoint
@app.route('/api/security', methods=['GET'])
def get_security():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM security_alerts ORDER BY alert_id DESC')
    alerts = cursor.fetchall()
    conn.close()
    return jsonify([dict(alert) for alert in alerts])

if __name__ == '__main__':
    print("Starting Flask REST API server on http://127.0.0.1:5000...")
    app.run(debug=True, port=5000)
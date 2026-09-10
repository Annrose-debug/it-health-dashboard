import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)
DB_NAME = "it_dashboard.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Returns rows as dictionary-like objects
    return conn

# 1. Health Status Endpoint
@app.route('/api/logs', methods=['GET'])
def get_logs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM system_logs ORDER BY id DESC LIMIT 20')
    logs = cursor.fetchall()
    conn.close()
    return jsonify([dict(log) for log in logs])

# 2. Support Tickets Endpoint
@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM support_tickets ORDER BY ticket_id DESC')
    tickets = cursor.fetchall()
    conn.close()
    return jsonify([dict(ticket) for ticket in tickets])

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
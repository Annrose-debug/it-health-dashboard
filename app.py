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

# 1. Health Status Logs Endpoint
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

# 4. Resolve Incident Ticket Endpoint (NEW - Day 12)
@app.route('/api/tickets/<int:ticket_id>/resolve', methods=['POST'])
def resolve_ticket(ticket_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE support_tickets SET status = 'RESOLVED' WHERE ticket_id = ?", (ticket_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": f"Ticket #{ticket_id} resolved."})

# 5. Dismiss Security Flag Endpoint (NEW - Day 12)
@app.route('/api/security/<int:alert_id>/dismiss', methods=['POST'])
def dismiss_security(alert_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM security_alerts WHERE alert_id = ?", (alert_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": f"Security alert #{alert_id} dismissed."})

if __name__ == '__main__':
    print("Starting Flask REST API server on http://127.0.0.1:5000...")
    app.run(debug=True, port=5000)
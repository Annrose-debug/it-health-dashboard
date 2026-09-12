# Real-Time IT Health & Security Monitoring Dashboard

A full-stack system health monitoring engine and threat detection dashboard built with Python, SQLite, Flask, and HTML/JS.

## Key Features
- **Endpoint Latency & Uptime Monitoring:** Automated HTTP status checking with microsecond accuracy (`monitor.py`).
- **Automated Incident Escalation:** Auto-generates structured IT support tickets upon detecting 5xx server errors or timeouts.
- **Security Log Analysis:** Audits access logs (`server_access.log`) for brute-force patterns and flags suspicious IP addresses (`security_parser.py`).
- **RESTful Metrics API:** Exposes system logs, active tickets, and security alerts via Flask (`app.py`).

## Tech Stack
- **Backend:** Python 3, Flask, SQLite3
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API)
- **Tools:** Git, GitHub, VS Code

## Quickstart
```bash
# Clone repository
git clone 
https://github.com/Annrose-debug/it-health-dashboard.git
cd it-health-dashboard

# Install dependencies
pip install -r requirements.txt

# Run REST API
python app.py

# ⚡ Cyber-Ops: Autonomous IT Health & Security Dashboard

A full-stack, real-time Security Operations Center (SOC) command center built during a rigorous 14-day engineering challenge. Designed with an **Obsidian & Amber** tactical aesthetic, this platform provides multi-target endpoint telemetry, automated incident escalation, and real-time log-based brute-force threat detection with interactive remediation controls.

---

## 🎨 Aesthetic & Design Philosophy
* **Palette:** Deep obsidian dark-mode backgrounds (`#0a0a0a` / `#121212`) paired with high-contrast tactical amber accents (`#eab308`) and crimson alert badges (`#ef4444`).
* **Typography:** Monospaced data readouts using `'JetBrains Mono'` paired with bold headers in `'Syne'`.
* **Layout:** CSS Grid dashboard layout optimized for high-density monitoring, live status counters, and asynchronous data updates.

---

## 🛠️ Technology Stack
* **Backend:** Python, Flask, SQLite (`it_dashboard.db`)
* **Background Automation:** Multi-process Python workers (`monitor.py`, `security_parser.py`)
* **Frontend:** HTML5, CSS3 (Custom Cyber Grid Theme), Asynchronous JavaScript (`fetch` API polling)
* **Architecture:** RESTful API, Non-blocking background worker loops, Relational database schema with automated migration handling

---

## 🚀 Core Features & Architecture

                   [Target Endpoints]
                           │
                    (HTTP Ping / Latency)
                           ▼
[monitor.py] ────────► (SQLite DB) ◄──────── [security_parser.py]
(Telemetry Worker)         │                 (Log Parser Engine)
▼
[Flask REST API]
│
(Async JS Polling)
▼
[Interactive Frontend UI]
(Executive KPIs & SOC Remediation)


1. **Live Multi-Target Telemetry (`monitor.py`):**
   * Continuously pings key service endpoints in the background.
   * Tracks millisecond response latencies and assigns operational status labels (`HEALTHY`, `WARNING/ERROR`, `CRITICAL_DOWN`).
2. **Autonomous Incident Escalation:**
   * Features smart ticket deduplication logic that automatically logs support incidents when endpoints fail or experience degradation.
3. **Brute-Force Threat Matrix (`security_parser.py`):**
   * Autonomous background worker parsing `server_access.log` using Python's `defaultdict`.
   * Tracks failed login attempts against security thresholds, flagging and locking out malicious IPs into the threat database.
4. **Interactive SOC Remediation:**
   * Actionable dashboard interface allowing security operators to instantly resolve open support tickets (`[RESOLVE]`) and clear security threats (`[DISMISS]`) via asynchronous `POST` requests without requiring full page reloads.

---

## 📁 Project Structure

```text
it-health-dashboard/
│
├── app.py                  # Flask backend REST API & template routing
├── monitor.py              # Background worker for multi-target endpoint telemetry
├── security_parser.py      # Background worker for log-based brute-force detection
├── server_access.log       # Simulated server access log stream
├── it_dashboard.db         # SQLite relational database
├── templates/
│   └── index.html          # Frontend command center UI & JS polling logic
└── README.md               # Project documentation
⚙️ Database Schema
system_logs: Stores historical endpoint ping telemetry (UID, service name, target URL, status code, latency in ms, status label, timestamp).

support_tickets: Tracks automated and manual incident escalations (ticket ID, service name, issue description, severity, status (OPEN / RESOLVED), creation timestamp).

security_alerts: Audits brute-force threats (alert ID, IP address, failed attempts count, alert level (CRITICAL), timestamp).

🚀 Quick Start Setup & Installation
To run this dashboard locally on your machine, follow these steps:

Clone the Repository:

Bash
git clone [https://github.com/YOUR_USERNAME/it-health-security-dashboard.git](https://github.com/YOUR_USERNAME/it-health-security-dashboard.git)
cd it-health-security-dashboard
Verify Prerequisites:
Ensure you have Python installed along with Flask (pip install flask).

Start Terminal 1 (Telemetry Background Worker):

Bash
python monitor.py
Start Terminal 2 (Security Threat Parser Engine):

Bash
python security_parser.py
Start Terminal 3 (Flask REST API Server):

Bash
python app.py
Access the Command Center:
Open your browser and navigate to:

Plaintext
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)
🛡️ License
This project is open-source and built as a portfolio demonstration of full-stack engineering and systems automation principles.

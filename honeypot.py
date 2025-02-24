from flask import Flask, request, jsonify, render_template
import logging
import os
import requests
from collections import defaultdict
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Konfigurasi logging
log_file = "honeypot.log"
logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(message)s")

# Rate Limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# In-memory storage for counting IP attacks to avoid reading the log file repeatedly
ip_attack_count = defaultdict(int)
ban_threshold = 5
whitelisted_ips = ["127.0.0.1"]  # Add your trusted IPs here

def log_attack(ip, endpoint, data, user_agent):
    if ip in whitelisted_ips:
        return

    log_entry = f"[ATTACK] IP: {ip} | Endpoint: {endpoint} | Data: {data} | User-Agent: {user_agent}"
    logging.info(log_entry)
    print(log_entry)
    
    # Update in-memory count
    ip_attack_count[ip] += 1
    
    # Auto-ban IP jika melebihi ambang batas
    if ip_attack_count[ip] >= ban_threshold:
        os.system(f"iptables -A INPUT -s {ip} -j DROP")
        logging.info(f"[BAN] IP {ip} telah diblokir setelah {ban_threshold} percobaan serangan.")
    
    # Kirim notifikasi ke WhatsApp (jika diaktifkan)
    CALLMEAPI_KEY = os.getenv("CALLMEAPI_KEY")
    CALLMEAPI_PHONE_NUMBER = os.getenv("CALLMEAPI_PHONE_NUMBER")
    if CALLMEAPI_KEY and CALLMEAPI_PHONE_NUMBER:
        message = f"⚠️ *Honeypot Alert!*\nIP: {ip}\nEndpoint: {endpoint}\nUser-Agent: {user_agent}"
        requests.post("https://api.callmebot.com/whatsapp.php", params={
            "phone": CALLMEAPI_PHONE_NUMBER,
            "text": message,
            "apikey": CALLMEAPI_KEY
        })

@app.route("/")
def home():
    return "Welcome to the fake server! Nothing to see here."

@app.route("/admin")
@limiter.limit("5 per minute")
def fake_admin():
    log_attack(request.remote_addr, "/admin", "Unauthorized access attempt", request.headers.get('User-Agent'))
    return "403 Forbidden", 403

@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def fake_login():
    if request.method == "POST":
        log_attack(request.remote_addr, "/login", request.form, request.headers.get('User-Agent'))
    return "Login failed", 401

@app.route("/db")
@limiter.limit("5 per minute")
def fake_database():
    log_attack(request.remote_addr, "/db", "Database access attempt", request.headers.get('User-Agent'))
    return "Database connection error", 500

@app.route("/robots.txt")
@limiter.limit("5 per minute")
def fake_robots():
    log_attack(request.remote_addr, "/robots.txt", "Scanning robots.txt", request.headers.get('User-Agent'))
    return "User-agent: *\nDisallow: /admin\nDisallow: /db"

@app.route("/config")
@limiter.limit("5 per minute")
def fake_config():
    log_attack(request.remote_addr, "/config", "Attempt to access configuration files", request.headers.get('User-Agent'))
    return "404 Not Found", 404

@app.route("/wp-login.php")
@limiter.limit("5 per minute")
def fake_wp_login():
    log_attack(request.remote_addr, "/wp-login.php", "WordPress login attempt", request.headers.get('User-Agent'))
    return "403 Forbidden", 403

@app.route("/backup.zip")
@limiter.limit("5 per minute")
def fake_backup():
    log_attack(request.remote_addr, "/backup.zip", "Attempt to download backup file", request.headers.get('User-Agent'))
    return "404 Not Found", 404

@app.route("/shell.php")
@limiter.limit("5 per minute")
def fake_shell():
    log_attack(request.remote_addr, "/shell.php", "Web shell upload attempt", request.headers.get('User-Agent'))
    return "403 Forbidden", 403

@app.route("/api/admin")
@limiter.limit("5 per minute")
def fake_api_admin():
    log_attack(request.remote_addr, "/api/admin", "API admin access attempt", request.headers.get('User-Agent'))
    return jsonify({"error": "Unauthorized access"}), 403

@app.route("/honeypot-stats")
def honeypot_stats():
    try:
        with open(log_file, "r") as f:
            logs = f.readlines()
        return jsonify({"total_attacks": len(logs), "logs": logs[-10:]})
    except FileNotFoundError:
        return jsonify({"message": "No attacks recorded yet."})

@app.route("/clear-logs", methods=["POST"])
def clear_logs():
    try:
        open(log_file, "w").close()
        ip_attack_count.clear()
        return jsonify({"message": "Logs cleared successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/dashboard")
def dashboard():
    try:
        with open(log_file, "r") as f:
            logs = f.readlines()
        return render_template('dashboard.html', total_attacks=len(logs), logs=logs[-10:], ip_attack_count=ip_attack_count)
    except FileNotFoundError:
        return render_template('dashboard.html', total_attacks=0, logs=[], ip_attack_count=ip_attack_count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
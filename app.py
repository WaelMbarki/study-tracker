from flask import Flask, jsonify, request

app = Flask(__name__)

# ══════════════════════════════════════════════════════════
# State
# ══════════════════════════════════════════════════════════
camera_active = False
last_habit    = "unknown"

# ══════════════════════════════════════════════════════════
# ESP32 → API
# ══════════════════════════════════════════════════════════

# ESP32 calls this when person is detected
@app.route('/person_detected', methods=['POST'])
def person_detected():
    global camera_active
    camera_active = True
    print("[+] Person detected → AI should start")
    return jsonify({"status": "ok"})

# ESP32 calls this when session ends
@app.route('/session_ended', methods=['POST'])
def session_ended():
    global camera_active, last_habit
    camera_active = False
    last_habit    = "unknown"
    print("[+] Session ended → AI should stop")
    return jsonify({"status": "ok"})

# ESP32 polls this to get habit from AI
@app.route('/get_habit', methods=['GET'])
def get_habit():
    return jsonify({"habit": last_habit})

# ══════════════════════════════════════════════════════════
# AI → API
# ══════════════════════════════════════════════════════════

# AI polls this to know if it should work
@app.route('/camera_status', methods=['GET'])
def camera_status():
    return jsonify({"active": camera_active})

# AI sends result here
@app.route('/habit_result', methods=['POST'])
def habit_result():
    global last_habit
    data       = request.json
    last_habit = data.get("habit", "unknown")
    print(f"[+] Habit received from AI: {last_habit}")
    return jsonify({"status": "ok"})

@app.route('/reset', methods=['POST'])
def reset():
    global camera_active, last_habit
    camera_active = False
    last_habit    = "unknown"
    print("[*] State reset!")
    return jsonify({"status": "reset"})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
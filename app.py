from flask import Flask, jsonify, request

app = Flask(__name__)

# ══════════════════════════════════════════════════════════
# State
# ══════════════════════════════════════════════════════════
camera_active    = False
current_schedule = {}
last_habit       = "unknown"

# ══════════════════════════════════════════════════════════
# ESP32 Routes
# ══════════════════════════════════════════════════════════
@app.route('/person_detected', methods=['POST'])
def person_detected():
    global camera_active
    camera_active = True
    print("[+] Person detected → Camera OPEN")
    return jsonify({"action": "open_camera"})

@app.route('/session_ended', methods=['POST'])
def session_ended():
    global camera_active
    camera_active = False
    print("[+] Session ended → Camera CLOSE")
    return jsonify({"action": "close_camera"})

@app.route('/get_habit', methods=['GET'])
def get_habit():
    global last_habit
    return jsonify({"habit": last_habit})  # don't reset here!

# ESP32 reads habit from here
@app.route('/get_habit', methods=['GET'])
def get_habit():
    global last_habit
    habit      = last_habit
    last_habit = "unknown"  # reset after ESP32 reads it
    return jsonify({"habit": habit})

# ══════════════════════════════════════════════════════════
# Python AI Routes
# ══════════════════════════════════════════════════════════
@app.route('/camera_status', methods=['GET'])
def camera_status():
    return jsonify({"active": camera_active})

# Python AI sends habit here
@app.route('/habit_result', methods=['POST'])
def receive_habit():
    global camera_active, last_habit
    data       = request.json
    last_habit = data.get("habit", "unknown")
    camera_active = False
    print(f"[+] Habit received: {last_habit}")
    return jsonify({"habit": last_habit})

# ══════════════════════════════════════════════════════════
# Mobile App Routes
# ══════════════════════════════════════════════════════════
@app.route('/update_schedule', methods=['POST'])
def update_schedule():
    global current_schedule
    current_schedule = request.json
    print("[*] Schedule updated by mobile app")
    return jsonify({"updated": True})

@app.route('/get_schedule', methods=['GET'])
def get_schedule():
    return jsonify(current_schedule)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
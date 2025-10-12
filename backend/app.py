# app.py - FINAL CODE FOR HOSTING

from flask import Flask, request, jsonify
from flask_cors import CORS 
from datetime import datetime

app = Flask(__name__)
CORS(app) 

# --- UPDATED Data Storage ---
# Now stores both organic and anorganic counts.
latest_trash_data = {
    "organic_trash_count": 0.0,
    "anorganic_trash_count": 0.0,
    "last_updated": "N/A"
}
# ----------------------------

# Endpoint 1: Receiving data from the Jetson (using POST)
@app.route('/update_count', methods=['POST'])
def update_count():
    """Receives JSON data from the robot and updates the stored counts."""
    if request.is_json:
        data = request.get_json()
        
        # Check for required fields and ensure they are numbers
        if ('organic_trash_count' in data and 
            'anorganic_trash_count' in data):
            
            try:
                global latest_trash_data
                
                # Convert inputs to floats (assuming the Jetson sends numbers)
                latest_trash_data['organic_trash_count'] = float(data['organic_trash_count'])
                latest_trash_data['anorganic_trash_count'] = float(data['anorganic_trash_count'])
                latest_trash_data['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                print(f"Data received: Organic={latest_trash_data['organic_trash_count']}, Anorganic={latest_trash_data['anorganic_trash_count']}")
                return jsonify({"message": "Data received and updated"}), 200
            except ValueError:
                 return jsonify({"error": "Trash counts must be numbers"}), 400
        else:
            return jsonify({"error": "Missing organic_trash_count or anorganic_trash_count fields"}), 400
    else:
        return jsonify({"error": "Request must be JSON"}), 415

# Endpoint 2: Sending data to the Website (using GET)
@app.route('/get_count', methods=['GET'])
def get_count():
    """Returns the latest stored trash count to the website as JSON."""
    return jsonify(latest_trash_data), 200
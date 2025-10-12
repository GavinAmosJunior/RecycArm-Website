# app.py - FINAL CODE WITH WIB TIMEZONE

from flask import Flask, request, jsonify
from flask_cors import CORS 
from datetime import datetime
import pytz # NEW IMPORT: Needed for timezone handling

app = Flask(__name__)
CORS(app) 

# --- UPDATED Data Storage ---
# Stores the latest trash counts and the WIB timestamp.
latest_trash_data = {
    "organic_trash_count": 0.0,
    "anorganic_trash_count": 0.0,
    "last_updated": "N/A"
}
# ----------------------------

# Define the target timezone (Jakarta is WIB: Western Indonesian Time)
WIB_TIMEZONE = pytz.timezone('Asia/Jakarta')

# Endpoint 1: Receiving data from the Jetson (using POST)
@app.route('/update_count', methods=['POST'])
def update_count():
    """Receives JSON data from the robot and updates the stored counts."""
    if request.is_json:
        data = request.get_json()
        
        # Check for required fields
        if ('organic_trash_count' in data and 
            'anorganic_trash_count' in data):
            
            try:
                global latest_trash_data
                
                # 1. Get current time, localize it to WIB
                now_wib = datetime.now(WIB_TIMEZONE)
                
                # 2. Format the WIB time string
                timestamp_wib = now_wib.strftime("%Y-%m-%d %H:%M:%S")

                # Update stored data
                latest_trash_data['organic_trash_count'] = float(data['organic_trash_count'])
                latest_trash_data['anorganic_trash_count'] = float(data['anorganic_trash_count'])
                latest_trash_data['last_updated'] = timestamp_wib # Save the WIB time
                
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
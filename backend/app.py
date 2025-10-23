# app.py - FINAL CODE FOR BIN FULLNESS PERCENTAGE

from flask import Flask, request, jsonify
from flask_cors import CORS 
from datetime import datetime
import pytz 

app = Flask(__name__)
CORS(app) 

# --- UPDATED Data Storage ---
# Stores the latest bin fullness percentages (0.0 to 100.0) and the WIB timestamp.
latest_trash_data = {
    # 'Organic' refers to the trash type that is NOT Plastic (Non-Recyclable)
    "organic_fullness_percent": 0.0,
    # 'Anorganic' refers to the Plastic/Recyclable type
    "anorganic_fullness_percent": 0.0,
    "last_updated": "N/A"
}
# ----------------------------

# Define the target timezone (Jakarta is WIB: Western Indonesian Time)
WIB_TIMEZONE = pytz.timezone('Asia/Jakarta')

# Endpoint 1: Receiving data from the Jetson (using POST)
@app.route('/update_fullness', methods=['POST'])
def update_fullness():
    """
    Receives JSON data from the robot containing bin fullness percentages 
    and updates the stored data.
    """
    if request.is_json:
        data = request.get_json()
        
        # Check for required percentage fields
        required_fields = ['organic_fullness_percent', 'anorganic_fullness_percent']
        if all(field in data for field in required_fields):
            
            try:
                global latest_trash_data
                
                # 1. Get current time, localize it to WIB
                now_wib = datetime.now(WIB_TIMEZONE)
                
                # 2. Format the WIB time string
                timestamp_wib = now_wib.strftime("%Y-%m-%d %H:%M:%S")

                # Update stored data with the new percentages
                latest_trash_data['organic_fullness_percent'] = float(data['organic_fullness_percent'])
                latest_trash_data['anorganic_fullness_percent'] = float(data['anorganic_fullness_percent'])
                latest_trash_data['last_updated'] = timestamp_wib 
                
                print(f"Data received: Organic Bin Fullness={latest_trash_data['organic_fullness_percent']}%, Anorganic Bin Fullness={latest_trash_data['anorganic_fullness_percent']}%")
                return jsonify({"message": "Bin fullness data received and updated"}), 200
            except ValueError:
                 return jsonify({"error": "Fullness percentages must be numbers"}), 400
        else:
            return jsonify({"error": f"Missing required fields: {', '.join(required_fields)}"}), 400
    else:
        return jsonify({"error": "Request must be JSON"}), 415

# Endpoint 2: Sending data to the Website (using GET)
@app.route('/get_fullness', methods=['GET'])
def get_fullness():
    """Returns the latest stored bin fullness data to the website as JSON."""
    return jsonify(latest_trash_data), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
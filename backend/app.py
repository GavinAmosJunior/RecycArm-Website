from flask import Flask, request, jsonify
from flask_cors import CORS 
from datetime import datetime
import pytz 

app = Flask(__name__)
CORS(app) 

# --- UPDATED Data Storage ---
# Stores the latest bin fullness percentages (0.0 to 100.0) and the WIB timestamp.
latest_trash_data = {
    # Existing Keys:
    "organic_fullness_percent": 0.0,
    "anorganic_fullness_percent": 0.0,
    
    # --- NEW KEY ADDED to store the Base64 encoded image string ---
    "camera_feed_base64": None, 
    
    "last_updated": "N/A"
}
# ----------------------------

# Define the target timezone (Jakarta is WIB: Western Indonesian Time)
WIB_TIMEZONE = pytz.timezone('Asia/Jakarta')

# ENDPOINT POST
@app.route('/update_fullness', methods=['POST'])
def update_fullness():
    """
    Receives JSON data from the robot containing bin fullness percentages,
    the Base64 image stream, and updates the stored data.
    """
    if request.is_json:
        data = request.get_json()
        
        # --- MODIFIED: Added 'camera_feed_base64' to required_fields ---
        required_fields = ['organic_fullness_percent', 'anorganic_fullness_percent', 'camera_feed_base64']
        
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
                
                # --- NEW: Store the Base64 image string ---
                latest_trash_data['camera_feed_base64'] = data['camera_feed_base64']
                
                latest_trash_data['last_updated'] = timestamp_wib 
                
                print(f"Data received: Organic Bin Fullness={latest_trash_data['organic_fullness_percent']}%, Anorganic Bin Fullness={latest_trash_data['anorganic_fullness_percent']}%. Image data stored.")
                return jsonify({"message": "Bin fullness and camera data received and updated"}), 200
            # --- MODIFIED: Now catches general Exception to handle non-string Base64 or number errors ---
            except (ValueError, TypeError) as e:
                 return jsonify({"error": f"Data processing failed. Check percentages (must be numbers) and Base64 string. Error: {e}"}), 400
        else:
            return jsonify({"error": f"Missing required fields: {', '.join(required_fields)}"}), 400
    else:
        return jsonify({"error": "Request must be JSON"}), 415

# ENDPOINT GET (NO CHANGES - It will now return the new key automatically)
@app.route('/get_fullness', methods=['GET'])
def get_fullness():
    """Returns the latest stored bin fullness data (including camera data) to the website as JSON."""
    return jsonify(latest_trash_data), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
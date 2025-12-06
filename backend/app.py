from flask import Flask, request, jsonify
from flask_cors import CORS 
from datetime import datetime
import pytz 

app = Flask(__name__)
CORS(app) 

# --- UPDATED Data Storage ---
# Stores the latest bin fullness percentages (0.0 to 100.0) and the WIB timestamp.
latest_trash_data = {
    # Existing Keys for Bin Fullness:
    "organic_fullness_percent": 0.0,
    "anorganic_fullness_percent": 0.0,
    
    # New Key to store the Base64 encoded image string (Starts as None)
    "camera_feed_base64": None, 
    
    # Timestamp reflects the LAST successful BIN FULLNESS update
    "last_updated": "N/A"
}
# ----------------------------

# Define the target timezone (Jakarta is WIB: Western Indonesian Time)
WIB_TIMEZONE = pytz.timezone('Asia/Jakarta')

# =========================================================================
# ENDPOINT 1: POST /update_fullness (Only for Percentages)
# =========================================================================
@app.route('/update_fullness', methods=['POST'])
def update_fullness():
    """
    Receives JSON data from the robot containing only bin fullness percentages
    and updates the stored data. This endpoint is now independent of the camera.
    """
    if request.is_json:
        data = request.get_json()
        
        # --- MODIFIED: REQUIRED FIELDS are now ONLY the two percentages ---
        required_fields = ['organic_fullness_percent', 'anorganic_fullness_percent']
        
        if all(field in data for field in required_fields):
            
            try:
                global latest_trash_data
                
                # 1. Get current time, localize it to WIB (Timestamp update)
                now_wib = datetime.now(WIB_TIMEZONE)
                
                # 2. Format the WIB time string
                timestamp_wib = now_wib.strftime("%Y-%m-%d %H:%M:%S")

                # Update stored data with the new percentages
                latest_trash_data['organic_fullness_percent'] = float(data['organic_fullness_percent'])
                latest_trash_data['anorganic_fullness_percent'] = float(data['anorganic_fullness_percent'])
                
                # Update the timestamp
                latest_trash_data['last_updated'] = timestamp_wib 
                
                print(f"Data received: Organic Bin Fullness={latest_trash_data['organic_fullness_percent']}%, Anorganic Bin Fullness={latest_trash_data['anorganic_fullness_percent']}%.")
                return jsonify({"message": "Bin fullness data received and updated"}), 200
            
            except (ValueError, TypeError) as e:
                 return jsonify({"error": f"Fullness percentages must be numbers. Error: {e}"}), 400
        else:
            return jsonify({"error": f"Missing required fields: {', '.join(required_fields)}. Camera stream should use /update_camera."}), 400
    else:
        return jsonify({"error": "Request must be JSON"}), 415

# =========================================================================
# ENDPOINT 2: POST /update_camera (Only for Image Stream)
# =========================================================================
@app.route('/update_camera', methods=['POST'])
def update_camera():
    """
    NEW ENDPOINT. Receives JSON data containing only the Base64 camera stream 
    and updates the stored data.
    """
    if request.is_json:
        data = request.get_json()
        
        # Only requires the camera key
        required_fields = ['camera_feed_base64']
        
        if all(field in data for field in required_fields):
            try:
                global latest_trash_data
                
                # Store the Base64 image string. We do NOT update 'last_updated' here.
                latest_trash_data['camera_feed_base64'] = data['camera_feed_base64']
                
                print("Camera data received and stored.")
                return jsonify({"message": "Camera stream data received"}), 200
            except Exception as e:
                return jsonify({"error": f"Camera data processing failed: {e}"}), 400
        else:
            return jsonify({"error": f"Missing required field: {', '.join(required_fields)}"}), 400
    else:
        return jsonify({"error": "Request must be JSON"}), 415
        
# =========================================================================
# ENDPOINT GET (Returns All Stored Data)
# =========================================================================
@app.route('/get_fullness', methods=['GET'])
def get_fullness():
    """Returns the latest stored data (percentages and camera stream) to the website as JSON."""
    return jsonify(latest_trash_data), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
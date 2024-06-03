from flask import Flask, request, jsonify
import requests
import datetime
import logging

app = Flask(__name__)
API_BASE_URL = "http://172.173.142.98:3000/api/v1"

@app.route('/add', methods=['POST'])
def add_praktikan():
    try:
        req_data = request.get_json()
        name = req_data.get('name')
        niu = req_data.get('niu')
        group_number = req_data.get('group_number')

        if not (name and niu and group_number):
            return jsonify({"error": "Missing one of the required fields"}), 400

        data = {
            "name": name,
            "niu": niu,
            "group_number": group_number
        }

        response = requests.post(f"{API_BASE_URL}/praktikan", json=data)
        
        if response.status_code == 404:
            logging.error(f"API endpoint not found: {API_BASE_URL}/praktikan")
            return jsonify({"error": "API endpoint not found"}), 404
        elif response.status_code != 201:
            logging.error(f"Unexpected response status: {response.status_code}, response: {response.text}")
            return jsonify({"error": "Unexpected response from API"}), response.status_code

        response_data = response.json()
        return jsonify(response_data), response.status_code

    except ValueError as e:
        logging.error(f"Value error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


        
@app.route('/get', methods=['GET'])
def get_praktikan():
    niu = request.args.get('niu')
    if not niu:
        return jsonify({"error": "Please pass a niu as query parameter"}), 400

    response = requests.get(f"{API_BASE_URL}/praktikan/{niu}")
    
    if response.status_code == 404:
        logging.error(f"API endpoint not found: {API_BASE_URL}/praktikan/{niu}")
        return jsonify({"error": "API endpoint not found"}), 404
    elif response.status_code == 500:
        logging.error(f"API internal server error: {response.text}")
        return jsonify({"error": "API internal server error"}), 500
    elif response.status_code != 200:
        logging.error(f"Unexpected response status: {response.status_code}, response: {response.text}")
        return jsonify({"error": "Unexpected response from API"}), response.status_code
    
    response_data = response.json()
    
    # Handle case where no data is found
    if not response_data:
        return jsonify({"error": "No data found for the provided NIU"}), 404

    return jsonify(response_data), response.status_code



if __name__ == '__main__':
    app.run(debug=True)

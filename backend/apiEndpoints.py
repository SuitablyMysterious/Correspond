from flask import Flask, request, jsonify
from database.packet.db import store_email_data  # Assuming you have a function for DB interaction

app = Flask(__name__)

@app.route('/store_email', methods=['POST'])
def store_email():
    try:
        # Get the email data from the request
        email_data = request.get_json()

        # Process/store the email data in the database
        store_email_data(email_data)  # Function you’ll define for DB interaction

        # Send a success response
        return jsonify({"message": "Email stored successfully!"}), 200
    except Exception as e:
        # If an error occurs, send an error response
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)

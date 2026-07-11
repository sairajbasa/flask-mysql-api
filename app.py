from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# --- Health Check Route ---
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "success",
        "message": "Flask User API is running!"
    }), 200
# --------------------------

# Database configuration
db_config = {
    'host': '<provide end point here>',
    'user': 'admin',
    'password': 'Cloud123',
    'database': 'flaskapp_db' # Must match the DB name you created in Workbench
}

def create_connection():
    """Establish a connection to the MySQL database."""
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
    except Error as e:
        print(f"Error: '{e}'")
    return connection

# POST: Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    useremail = data.get('useremail')

    if not username or not useremail:
        return jsonify({'error': 'Please provide username and useremail'}), 400

    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO user (username, useremail) VALUES (%s, %s)"
        cursor.execute(query, (username, useremail))
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({'message': 'User created successfully', 'userid': user_id}), 201
    return jsonify({'error': 'Database connection failed'}), 500

# GET: Retrieve all users
@app.route('/users', methods=['GET'])
def get_users():
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(users), 200
    return jsonify({'error': 'Database connection failed'}), 500

# GET: Retrieve a specific user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user WHERE userid = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return jsonify(user), 200
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'error': 'Database connection failed'}), 500

# PUT: Update an existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    username = data.get('username')
    useremail = data.get('useremail')

    if not username or not useremail:
        return jsonify({'error': 'Please provide username and useremail'}), 400

    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE user SET username = %s, useremail = %s WHERE userid = %s"
        cursor.execute(query, (username, useremail, user_id))
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()

        if affected_rows > 0:
            return jsonify({'message': 'User updated successfully'}), 200
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'error': 'Database connection failed'}), 500

# DELETE: Remove a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user WHERE userid = %s", (user_id,))
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()

        if affected_rows > 0:
            return jsonify({'message': 'User deleted successfully'}), 200
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'error': 'Database connection failed'}), 500

if __name__ == '__main__':
    # Listens on all interfaces so it can be accessed within a VPC/network
    app.run(host='0.0.0.0', port=5000, debug=True)

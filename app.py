from flask import Flask, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )

@app.route('/petitions', methods=['GET'])
def get_petitions():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM petitions')
    petitions = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(petitions)

@app.route('/petitions', methods=['POST'])
def add_petition():
    title = request.json['title']
    description = request.json['description']
    
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('INSERT INTO petitions (title, description) VALUES (%s, %s)', (title, description))
    db.commit()
    cursor.close()
    db.close()
    
    return jsonify({'message': 'Petition added successfully!'}), 201

if __name__ == '__main__':
    app.run()

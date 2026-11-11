from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DB_NAME = 'Student System.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/students', methods=['GET', 'POST'])
def handle_students():
    conn = get_db_connection()
    
    if request.method == 'GET':
        cursor = conn.execute('SELECT * FROM students')
        rows = cursor.fetchall()
        conn.close()
        
        student_list = []
        for row in rows:
            student_list.append({
                'id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'email': row[3]
            })
        return jsonify(student_list)

    elif request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')

        conn.execute('INSERT INTO students (first_name, last_name, email) VALUES (?, ?, ?)',
                     (first_name, last_name, email))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Student added successfully!'})

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    conn = get_db_connection()
    data = request.get_json()
    
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')

    conn.execute('''
        UPDATE students 
        SET first_name = ?, last_name = ?, email = ? 
        WHERE id = ?
    ''', (first_name, last_name, email, student_id))
    
    conn.commit()
    conn.close()
    return jsonify({'message': 'Student updated successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
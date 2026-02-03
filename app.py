from flask import Flask, request, jsonify, send_from_directory
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'todos.json'

def load_todos():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = load_todos()
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.json
    todos = load_todos()

    new_todo = {
        'id': len(todos) + 1,
        'text': data.get('text', ''),
        'completed': False,
        'created_at': datetime.now().isoformat()
    }

    todos.append(new_todo)
    save_todos(todos)

    return jsonify(new_todo), 201

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.json
    todos = load_todos()

    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = data.get('completed', todo['completed'])
            save_todos(todos)
            return jsonify(todo)

    return jsonify({'error': 'Todo not found'}), 404

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todos = load_todos()
    todos = [t for t in todos if t['id'] != todo_id]
    save_todos(todos)

    return '', 204

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

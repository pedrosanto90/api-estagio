from flask import Flask, request, jsonify
from database import getAllTodos, createTodo, getTodo, updateTodo, deleteTodo, getAllUsers, getUser, createUser, updateUser, deleteUser

app = Flask(__name__)

@app.route('/api/todos/', methods=['GET', 'POST'])
@app.route('/api/todos/<id>', methods=['GET', 'PUT', 'DELETE'])
def todos(id=None):
    if request.method == 'GET':
        user_id = request.args.get('user')
        if id and not user_id:
            # Get a todo by id
            return jsonify(getTodo(id))
        else:
            # Get all todos from user
            return jsonify(getAllTodos(user_id))

    # Create a new todo
    elif request.method == 'POST':
        data = request.get_json()
        user_id = data.get('user_id')
        title = data.get('title')
        description = data.get('description')
        estado = data.get('estado')
        data = data.get('data_finalizacao')
        createTodo(user_id, title, description, estado, data)
        return jsonify({'message': 'Todo created successfully'})

    elif request.method == 'PUT' and id:
        data = request.get_json()
        updateTodo(id, data)
        return jsonify({'message': 'Update todo by id'})
    elif request.method == 'DELETE' and id:
         return deleteTodo(id)


@app.route('/api/users/', methods=['GET', 'POST'])
@app.route('/api/users/<id>', methods=['GET', 'PUT', 'DELETE'])
def users(id=None):
    if request.method == 'GET' and id:
        return jsonify(getUser(id))

    elif request.method == 'GET':
        return jsonify(getAllUsers())

    elif request.method == 'POST':
        data = request.get_json()
        return jsonify(createUser(data))

    elif request.method == 'PUT' and id:
        data = request.get_json()
        return jsonify(updateUser(id, data))

    elif request.method == 'DELETE' and id:
        return jsonify(deleteUser(id))

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)

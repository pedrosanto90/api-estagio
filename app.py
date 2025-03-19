from flask import Flask, request, jsonify
from database import getAllTodos, createTodo, getTodo, updateTodo, deleteTodo, getAllUsers, getUser, createUser, updateUser, deleteUser, getPassword
from utils import check_password
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "your-secret-key"

@app.route('/api/todos/', methods=['GET', 'POST'])
@app.route('/api/todos/<id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def todos(id=None):
    if request.method == 'GET':
        user_id = request.args.get('user')
        if id and not user_id:
            # Get a todo by id
            return jsonify(getTodo(id))
        elif user_id:
            # Get all todos from user
            return jsonify(getAllTodos(user_id))
        else:
            return jsonify({'message': 'User id is required'})

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

@app.route('/api/users/create', methods=['POST'])
def create_user():
    data = request.get_json()
    return jsonify(createUser(data))

@app.route('/api/users/', methods=['GET', 'POST'])
@app.route('/api/users/<id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def users(id=None):
    if request.method == 'GET' and id:
        return jsonify(getUser(id))

    elif request.method == 'GET':
        return jsonify(getAllUsers())

    elif request.method == 'PUT' and id:
        data = request.get_json()
        return jsonify(updateUser(id, data))

    elif request.method == 'DELETE' and id:
        return jsonify(deleteUser(id))

@app.route('/api/users/login', methods=['POST'])
def userLogin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password').encode('utf-8')  
    hashedPassword = getPassword(email)  

    if not hashedPassword:
        return jsonify({'message': f'User {email} not found'})

    if not check_password(password, hashedPassword[0]['password']):
        return jsonify({'message': 'Invalid email or password'})

    access_token = create_access_token(identity="user")
    return jsonify({'message': f'User {email} login successfully',
                    'access_token': access_token, 
                    'user_id': hashedPassword[0]['id'],
                    'userEmail': hashedPassword[0]['email'],
                    'name': hashedPassword[0]["nome"],
                    'last_name': hashedPassword[0]['ultimo_nome']
                    })

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)

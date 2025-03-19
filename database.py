import psycopg2
from dotenv import load_dotenv
import os
from utils import hash_password

load_dotenv()

connection = psycopg2.connect(database=os.getenv('DATABASE'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), host=os.getenv('DB_HOST'), port=os.getenv('PORT'))

cursor = connection.cursor()

# CRUD operations for todos 
def getAllTodos(user_id):
    sql_context = 'SELECT row_to_json(t) FROM (SELECT * FROM public.todos WHERE user_id = %s) t;'
    cursor.execute(sql_context, (user_id,))
    # Fetch all rows from database
    data = tuple(row[0] for row in cursor.fetchall())
    return data

def createTodo(user_id, title, description, estado, data):
    cursor.execute('INSERT INTO public.todos (user_id, title, description, estado, data_finalizacao) VALUES (%s, %s, %s, %s, %s);',
                    (user_id, title, description, estado, data))
    connection.commit()
    return {'message': 'Todo created successfully'}

def getTodo(id):
    cursor.execute('SELECT row_to_json(t) FROM (SELECT * FROM public.todos WHERE id = %s) t;', (id,))
    data = cursor.fetchone()
    return data 

def updateTodo(id, data):
    estado = data.get('estado')
    title = data.get('title')
    description = data.get('description')

    cursor.execute('UPDATE public.todos SET estado = %s, title = %s, description = %s WHERE id = %s;', (estado, title, description, id))
    connection.commit()
    return {'message': 'Todo updated successfully'}

def deleteTodo(id):
    cursor.execute('DELETE FROM public.todos WHERE id = %s;', (id,))
    connection.commit()
    return {'message': 'Todo deleted successfully'}

# CRUD operations for users
def getAllUsers():
    cursor.execute('SELECT row_to_json(u) FROM (SELECT * FROM public.users) u;')
    data = tuple(row[0] for row in cursor.fetchall())
    return data

def getUser(id):
    cursor.execute('SELECT row_to_json(u) FROM (SELECT * FROM public.users WHERE id = %s) u;', (id,))
    data = cursor.fetchone()
    return data

def createUser(data):
    username = data.get('username')
    name = data.get('nome')
    lastName = data.get('ultimo_nome')
    email = data.get('email')
    password = hash_password(data.get('password'))
    
    cursor.execute('INSERT INTO public.users \
            (username, nome, ultimo_nome, email, password) \
            VALUES (%s, %s, %s, %s, %s);',\
            (username, name, lastName, email, password))
    connection.commit()
    return {'message': 'User created successfully'}

def updateUser(id, data):
    username = data.get('username')
    name = data.get('nome')
    lastName = data.get('ultimo_nome')
    email = data.get('email')
    password = data.get('password')
    
    cursor.execute('UPDATE public.users SET username = %s, nome = %s, ultimo_nome = %s, email = %s, password = %s WHERE id = %s;',\
            (username, name, lastName, email, password, id))
    connection.commit()
    return {'message': 'User updated successfully'}

def deleteUser(id):
    cursor.execute('DELETE FROM public.users WHERE id = %s;', (id,))
    connection.commit()
    return {'message': 'User deleted successfully'}

def getPassword(email):
    cursor.execute('SELECT password FROM public.users WHERE email = %s;', (email,))
    data = cursor.fetchone()
    return data

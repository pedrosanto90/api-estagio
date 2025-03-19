import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    hashedPassword = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashedPassword.decode('utf-8')

def check_password(password, hashed):
    if isinstance(hashed, tuple):  
        hashed = hashed[0]  

    if isinstance(hashed, str):  
        hashed = hashed.encode('utf-8')  
    
    return bcrypt.checkpw(password, hashed)

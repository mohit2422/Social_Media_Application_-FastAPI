from passlib.context import CryptContext

#we are using bcrypt hashing algorithm 
# Create an instance of the CryptContext class
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
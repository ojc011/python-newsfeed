from app.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates
import bcrypt

salt = bcrypt.gensalt()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    
    @validates('email')
    def validate_email(self, key, email): #This will ensure email address contains @ sign
        assert '@' in email
        
        return email
    
    @validates('password')
    def validate_password(self, key, password): #Ensures length of pw is more than 4 chars
        assert len(password) > 4
        
        return bcrypt.hashpw(password.encode('utf-8'), salt) # Hashes and encrypts pw using bcrypt module
        
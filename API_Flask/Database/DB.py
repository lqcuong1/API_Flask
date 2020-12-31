import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
import time
# pip install PyJWT
import jwt

# The Engine is how SQLAlchemy communicates with your database
engine = create_engine(
    # telling where your database currently is located.
    'sqlite:///D:\\API_Flask\\Database\\db.sqlite3',
    # The attribute echo=True will make SQLAlchemy to log all SQL commands
    echo=True,
    # By default, check_same_thread is True and only the creating thread may use the connection.
    # If set False, the returned connection may be shared across multiple threads.
    connect_args={'check_same_thread': False}
)

# the thing that makes SQLAlchemy so attractive is its ORM
# The ORM must have a session
Session = sessionmaker(bind=engine)
session = Session()

# To map which table in the db will be related to each class in our files,
# we will use a SQLAlchemy system called Declarative
Base = declarative_base()


# class User that inherits from our Base declarative
class Account(Base):
    # must add __tablename__ (REQUIRED)
    __tablename__ = 'Account'

    id = Column(String, primary_key=True)
    username = Column(String(100))
    password_hash = Column(String(50))
    full_name = Column(String(200))
    is_admin = Column(Boolean)

    def __init__(self, id, username, input_password, full_name, is_admin):
        self.id = id
        self.username = username
        self.hash_password(input_password)
        self.full_name = full_name
        self.is_admin = is_admin

    # region BASIC AUTHENTICATION

    def hash_password(self, raw_password):
        # function of werkzeug.security lib
        # => return a hashed password (same password => return many different hashed passwords)
        self.password_hash = generate_password_hash(raw_password)

    def verify_password(self, input_password):
        # function of werkzeug.security lib
        # => compare password, return True/False
        return check_password_hash(self.password_hash, input_password)

    # endregion

    # region TOKEN AUTHENTICATION - HS256 (HMAC SHA-256) algorithm

    def generate_auth_token(self, expires_in=600, secret_key=""):
        return jwt.encode({'id': self.id, 'username': self.username, 'exp': time.time() + expires_in}, secret_key, algorithm='HS256')

    @staticmethod
    def verify_auth_token(token, secret_key):
        try:
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
        except Exception as e:
            print("=====> Error! ", e)
            return ""
        print("=====> Expiration Time: " + str(data['exp'] - time.time()))
        return data['id']

    # endregion


class Subject(Base):
    __tablename__ = 'Subject'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    teacher = Column(String(100))
    required = Column(Boolean)

    def __init__(self, name, teacher, required):
        self.name = name
        self.teacher = teacher
        self.required = required

    def __repr__(self):
        return f'Subject {self.name}'

    def json_format(self):
        return {
                   'id': self.id,
                   'name': self.name,
                   'teacher': self.teacher,
                   'required': self.required
                }


def init_value():
    session.add(Account("TMA_2018", "abc", "123", "Nguyen Van A", True))
    session.add(Account("TMA_2019", "def", "123", "Tran Van B", False))
    session.add(Account("TMA_2020", "ghi", "123", "Nguyen Thi C", True))

    session.add(Subject("Math", "John", True))
    session.add(Subject("Chemistry", "Cindy", False))
    session.add(Subject("Biology", "Tony", True))

    session.commit()


if __name__ == '__main__':
    # create sqlite3 file
    if not os.path.exists('db.sqlite3'):
        Base.metadata.create_all(engine)
        init_value()

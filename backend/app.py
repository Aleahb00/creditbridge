from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')

jwt = JWTManager(app)
bcrypt = Bcrypt(app)

from routes import auth_bp
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
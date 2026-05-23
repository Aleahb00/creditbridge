from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

load_dotenv()

print("MONGO_URI:", os.getenv('MONGO_URI'))

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

mongo = PyMongo(app)

@app.route('/api/hello')
def hello():
    try:
        mongo.cx.admin.command('ping')
        return {'message': 'MongoDB connected successfully!'}
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
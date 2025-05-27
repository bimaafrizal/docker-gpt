# print("Halo, ini program Python di Docker!")

# for i in range(5):
#     print(f"Baris ke-{i+1} dari Docker container")


from flask import Flask, jsonify
from pymongo import MongoClient
import redis
import os

app = Flask(__name__)

mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/testdb')
client = MongoClient(mongo_uri)
db = client.testdb
users_collection = db.users

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
r = redis.Redis(host=redis_host, port=redis_port)

@app.route('/')
def hello():
    # return "Halo dari Flask di Docker!"
    users = list(users_collection.find({}, {'_id': 0}))
    cache_count = r.get('count') or 0
    return jsonify({
        'users': users,
        'cache_count': int(cache_count)
    })

@app.route('/add/<name>')
def add_user(name):
    users_collection.insert_one({'name': name})
    r.incr('count')  # tambah hitungan di Redis
    return jsonify({'message': f'User {name} added!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

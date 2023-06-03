from flask import Flask, render_template, request, redirect
import os
from urllib.parse import urlparse
from db import Postgres
from redis import Redis
import json


app = Flask(__name__)
db_conection: Postgres = None
redis_connection: Redis = None


def get_content():
    return db_conection.select("users")


@app.route('/')
def home():
    keys = redis_connection.keys()
    result = {}
    for key in keys:
        data = redis_connection.get(key)

        result.update({
            int(key): json.loads(data)
        })

    return render_template('index.html', content=result)


@app.route('/reload', methods=["GET"])
def reload():
    content = get_content()
    for info in content:
        id_ = info[0]
        data = {
            "name": info[1],
            "surename": info[2],
            "age": int(info[3])
        }
        redis_connection.set(str(id_), json.dumps(data))
    return redirect('/')
    

@app.route('/add', methods=["POST"])
def add():
    name = request.form.get("name")
    surename = request.form.get("surename")
    age = request.form.get("age")
    if all([name, surename, age]):  
        data = {
            "name": name, 
            "surename": surename, 
            "age": int(age)
        }

        id_ = db_conection.insert("users", data=data, additinal_query="RETURNING id")[0]
        redis_connection.set(str(id_), json.dumps(data))
    return redirect('/')


@app.route('/delete/<id_>')
def delete(id_):
    db_conection.delete("users", data={"id": int(id_)})
    redis_connection.delete(id_)
    return redirect('/')


@app.route('/clean')
def clean():
    db_conection.cleanup()
    db_conection.create_tables()
    return redirect('/')


def init():
    db_url = os.getenv("DATABASE_URL")
    if db_url is None:
        raise LookupError("[ERROR]: DATABASE_URL needs to be set!")

    result = urlparse(db_url)

    global db_conection
    db_conection = Postgres(host=result.hostname,
                            database=result.path[1:],
                            port=result.port,
                            user=result.username,
                            password=result.password)
    
    global redis_connection
    redis_connection = Redis(host=os.getenv("REDIS_HOST", "localhost"), port=os.getenv("REDIS_PORT", 6379))


if __name__ == "__main__":
    init()
    app.run(debug=True, host="0.0.0.0", port="5000")

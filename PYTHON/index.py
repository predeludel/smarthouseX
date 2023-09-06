from flask import render_template, request
from flask_socketio import SocketIO
import json
import logging
from model import *
from model import db

socket = SocketIO(app, cors_allowed_origins="*")

users_status = []
HOST = "172.20.10.3"
PORT = 5001


@app.route('/')
def show_main():
    return render_template('main.html')


@app.route("/security")
def stream_page():
    return render_template("security.html")


@app.route('/robot')
def show_robot():
    return render_template('robot.html')


@app.route('/index')
def show_index():
    return render_template('index.html')


logging.basicConfig(level=logging.DEBUG)


@app.route("/alisa", methods=["POST"])
def main():
    logging.info(request.json)

    response = {
        "version": request.json["version"],
        "session": request.json["session"],
        "response": {
            "end_session": False
        }
    }
    req = request.json
    if req["session"]["new"]:
        response["response"]["text"] = "Я могу вам помочь!"
    else:
        if req["request"]["original_utterance"].lower() in ["включи свет в кухне"]:
            socket.emit("light", {'status': 1})
            response["response"]["text"] = "Сделано"
        elif req["request"]["original_utterance"].lower() in ["выключи свет в кухне"]:
            socket.emit("light", {'status': 0})
            response["response"]["text"] = "Сделано"

    return json.dumps(response)


@socket.event
def connect():
    db_data = Data.query.filter_by(id=1).first()
    socket.emit("getData",
                {"air_temp": db_data.air_temp, "humidity": db_data.humidity, "light": db_data.light,
                 "light1": db_data.light1, "light2": db_data.light2, "light3": db_data.light3, "lock": db_data.lock,
                 "coffee": db_data.coffee})
    socket.emit("send_photo", "ghedtn")


@socket.event
def data_sensors(data):
    save_data(data)
    socket.emit("getData",
                {"air_temp": data["air_temp"], "humidity": data["humidity"], "light": data["light"],
                 "light1": data["light1"], "light2": data["light2"], "light3": data["light3"], "lock": data["lock"],
                 "coffee": data["coffee"]})
    print(data)


@socket.event
def light(data):
    socket.emit("light", {'status': data['status']})


@socket.event
def lock(data):
    socket.emit("lock", {'status': data['status']})


@socket.event
def coffee(data):
    socket.emit("coffee", {'status': data['status']})


@socket.event
def light1(data):
    socket.emit("light1", {'status': data['status']})


@socket.event
def light2(data):
    socket.emit("light2", {'status': data['status']})


@socket.event
def light3(data):
    socket.emit("light3", {'status': data['status']})


@socket.event
def auth(data):
    for i in users_status:
        if i["name"] == data["name"]:
            i["sid"] = request.sid
    if data["name"] not in [i["name"] for i in users_status]:
        users_status.append({"name": data["name"], "sid": request.sid})
    db_data = Data.query.filter_by(id=1).first()
    print(db_data.light, db_data.lock)
    socket.emit("light", {'status': db_data.light})
    socket.emit("lock", {'status': db_data.lock})
    socket.emit("light1", {'status': db_data.light1})
    socket.emit("light2", {'status': db_data.light2})
    socket.emit("coffee", {'status': db_data.coffee})
    print(users_status)


def save_data(record):
    if Data.query.filter_by(id=1).first() is None:
        data = Data(air_temp=float(record["air_temp"]),
                    humidity=float(record["humidity"]), light=int(record["light"]),
                    light1=int(record["light1"]), light2=int(record["light2"]), light3=int(record["light3"]),
                    lock=int(record["lock"]), coffee=int(record["coffee"]))
        db.session.add(data)
        db.session.commit()
    else:
        print("я обновилась ура")
        Data.query.filter_by(id=1).first().update(float(record["air_temp"]), float(record["humidity"]),
                                                  int(record["light"]), int(record["light1"]), int(record["light2"]),
                                                  int(record["light3"]),
                                                  int(record["lock"]), int(record["coffee"]))


@socket.event
def send_photo(data):
    print("пришло фото")
    socket.emit('camera', data)


@socket.event
def push_camera():
    print("хочу фото")
    socket.emit('push_camera')


@socket.event
def lock_names(names):
    socket.emit('lock_names', names)


if __name__ == '__main__':
    app.app_context().push()
    db.create_all()
    socket.run(app, debug=True, host=HOST, port=PORT)

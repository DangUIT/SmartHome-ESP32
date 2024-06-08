from flask import Flask, render_template, Response, stream_with_context, request, url_for, redirect, jsonify
from flask_mqtt import Mqtt
import json
import sqlite3
import time

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'mqtt.flespi.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = '42X56PIbNHS7v88dv6biL872LnxkHlsoDwX5msuTMmBAW5zszyLl8f2FsPz8b7Ll'
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
mqtt = Mqtt(app)


def get_db_connection():
    connect = sqlite3.connect('sensors.db')
    connect.row_factory = sqlite3.Row
    return connect

@app.route('/')
def index():
    return render_template('login.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "123":
            return redirect(url_for("home"))
    return render_template("login.html")
    
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/grapth')
def grapth():
    def get_database():
        while True:
            conn = get_db_connection()
            temp_data = conn.execute('SELECT TIME, TEMPERATURE FROM SENSOR \
                WHERE id = (SELECT MAX(id) FROM SENSOR)').fetchone()
            humi_data = conn.execute('SELECT TIME, HUMIDITY FROM SENSOR \
                WHERE id = (SELECT MAX(id) FROM SENSOR)').fetchone()
            json_data = json.dumps(
                {'temp_time': temp_data['TIME'], 'temp_value': float(temp_data['TEMPERATURE'].replace("C","")), \
                'humi_time': humi_data['TIME'], 'humi_value': float(humi_data['HUMIDITY'].replace("%",""))})
            yield f"data:{json_data}\n\n"
            time.sleep(10)

    response = Response(stream_with_context(get_database()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

@app.route('/get-device-status', methods=['GET'])
def get_device_status():
    conn = get_db_connection()

    light_status = conn.execute('SELECT LIGHT FROM LIGHT ORDER BY ID DESC LIMIT 1').fetchone()[0]
    light_status = "ON" if light_status == "1" else "OFF"

    fan_status = conn.execute('SELECT FAN FROM FAN ORDER BY ID DESC LIMIT 1').fetchone()[0]
    if fan_status == "0": fan_status = "OFF"
    elif fan_status == "1": fan_status = "MODE 1"
    elif fan_status == "2": fan_status = "MODE 2"
    elif fan_status == "3": fan_status = "MODE 3"

    door_status = conn.execute('SELECT DOOR FROM DOOR ORDER BY ID DESC LIMIT 1').fetchone()[0]
    door_status = "CLOSE" if door_status == "0" else "OPEN"

    conn.close()
    return jsonify(light=light_status, fan=fan_status, door=door_status)

@app.route('/toggle-light', methods=['POST'])
def toggle_light():
    data = request.get_json()
    light_status = data.get('lightStatus')
    mqtt.publish('control', f"Light: {'1' if light_status else '0'}")
    return jsonify(success=True)

@app.route('/toggle-fan', methods=['POST'])
def toggle_fan():
    fan_data = request.get_json()
    fan_status = fan_data.get('fanStatus')
    fan_speed = fan_data.get('fanSpeed')
 
    if fan_status in (True, None):
        if fan_speed is not None:
            mqtt.publish('control', f"Fan: On, Mode: {fan_speed}")
    elif fan_status == False:
        mqtt.publish('control', 'Fan: Off, Mode: 0')
         
    return jsonify(success=True)

@app.route('/toggle-door', methods=['POST'])
def toggle_door():
    data = request.get_json()
    door_status = data.get('doorStatus')
    mqtt.publish('control', f"Door: {'1' if door_status else '0'}")
    return jsonify(success=True)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('dht')
    mqtt.subscribe('control')
    mqtt.subscribe('light')
    mqtt.subscribe('fan')
    mqtt.subscribe('door')


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):

    con = sqlite3.connect('sensors.db')
    cursor = con.cursor()

    if message.topic == 'control':
        message = message.payload.decode()
        # print(message)
    elif message.topic == 'dht':
    #Handle data
        message = message.payload.decode()
        message = message.split('\n')
        humi = message[0].split(':')
        temp = message[1].split(':')
        temp = temp[1].replace(" ",'')
        humi = humi[1].replace(" ","")
        cursor.execute("INSERT INTO SENSOR (TEMPERATURE,HUMIDITY) VALUES (?,?)", (temp,humi)) 

    elif message.topic == 'light':
        light = message.payload.decode()
        cursor.execute("INSERT INTO LIGHT (LIGHT) VALUES (?)", (light)) 

    elif message.topic == 'fan':
        fan = message.payload.decode()
        cursor.execute("INSERT INTO FAN (FAN) VALUES (?)", (fan)) 

    elif message.topic == 'door':
        door = message.payload.decode()
        cursor.execute("INSERT INTO DOOR (DOOR) VALUES (?)", (door)) 

    con.commit()
if __name__ == '__main__':
    app.run()
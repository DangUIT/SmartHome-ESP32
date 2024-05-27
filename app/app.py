from flask import Flask, render_template, Response, stream_with_context, request, url_for, redirect
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
            temp_data = conn.execute('SELECT TIME, TEMPERATURE FROM DATABASE \
                WHERE id = (SELECT MAX(id) FROM DATABASE)').fetchone()
            humi_data = conn.execute('SELECT TIME, HUMIDITY FROM DATABASE \
                WHERE id = (SELECT MAX(id) FROM DATABASE)').fetchone()
            json_data = json.dumps(
                {'temp_time': temp_data['TIME'], 'temp_value': float(temp_data['TEMPERATURE'].replace("C","")), \
                'humi_time': humi_data['TIME'], 'humi_value': float(humi_data['HUMIDITY'].replace("%",""))})
            yield f"data:{json_data}\n\n"
            time.sleep(10)

    response = Response(stream_with_context(get_database()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('dht')
   
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
                topic=message.topic,
                payload=message.payload.decode()
                )

    #Handle data
    message = data["payload"]
    message = message.split('\n')
    humi = message[0].split(':')
    temp = message[1].split(':')
    temp = temp[1].replace(" ",'')
    humi = humi[1].replace(" ","")
    
    with sqlite3.connect("sensors.db") as users: 
        cursor = users.cursor() 
        cursor.execute("INSERT INTO DATABASE (TEMPERATURE,HUMIDITY) VALUES (?,?)", 
                        (temp,humi)) 
        users.commit() 


if __name__ == '__main__':
    app.run()
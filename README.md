
![Screenshot 2024-06-12 173223](https://github.com/DangUIT/SmartHome-ESP32/assets/110042317/d3bf6806-d3d5-4a8f-8c7a-1e18fb28ea42)
# Smart Home System

This project demonstrates a smart home system using ESP32 to control and monitor various devices. The system utilizes sensors, actuators, and an MQTT protocol for communication between components. It also includes a web interface for end-user interaction.

## Features

- **Temperature and Humidity Monitoring:** Displayed on an SSD1306 OLED screen connected to the ESP32.
- **Light Control:** Using GPIO pins to toggle LEDs.
- **Fan Control:** Via a DC motor and L298N motor driver.
- **Door Control:** Managed with a servo motor controlled by PWM signals.
- **Web Interface:** Built with Flask for end-user interaction.
- **Data Transmission:** Using MQTT protocol for seamless communication.
- **Data Storage:** SQLite database for saving logs and configurations.

## System Architecture

### Components

1. **ESP32 Microcontroller**
   - Connects to sensors and actuators.
   - Publishes and subscribes to MQTT topics for communication.

2. **Sensors**
   - Collect environmental data like temperature and humidity.

3. **Actuators**
   - **LED Lights:** Controlled via GPIO pins.
   - **DC Motor:** Driven by L298N for fan control.
   - **Servo Motor:** Used for door control.

4. **SSD1306 OLED Display**
   - Displays temperature and humidity data in real-time.

5. **Server**
   - Hosts the Flask web application for user interaction.
   - Connects to an MQTT broker for communication with the ESP32.
   - Stores data in an SQLite database.

6. **MQTT Broker**
   - Facilitates data exchange between the ESP32 and the server.

### Workflow

1. Sensors gather data and send it to the ESP32.
2. The ESP32 processes the data and displays it on the OLED screen.
3. Commands from the web interface are sent to the ESP32 via MQTT.
4. The ESP32 controls actuators (lights, fan, door) based on commands.
5. The server logs actions and sensor data in the SQLite database.

## Requirements

### Hardware
- ESP32
- SSD1306 OLED Display
- L298N Motor Driver
- Servo Motor
- DC Motor
- Sensors (e.g., temperature and humidity sensor)
- LEDs

### Software
- Python (for the server and web interface)
- Flask
- SQLite
- MQTT Broker (e.g., Mosquitto)
- ESP-IDF framework for ESP32 development

## Installation

1. **Set Up MQTT Broker**
   - Install Mosquitto or another MQTT broker.
   - Configure topics for communication.

2. **Deploy the Flask Web Server**
   - Install dependencies: `pip install flask sqlite3 paho-mqtt`.
   - Run the Flask server: `python app.py`.

3. **Program the ESP32**
   - Use the ESP-IDF framework to upload the code to the ESP32.
   - Ensure correct WiFi and MQTT broker configurations.

4. **Connect Hardware Components**
   - Wire the sensors, actuators, and display as per the schematic.

## Usage

1. Start the MQTT broker.
2. Run the Flask server.
3. Power on the ESP32.
4. Access the web interface to monitor and control devices:
   - Toggle lights.
   - Adjust fan speed.
   - Control door position.
   - View temperature and humidity readings.

## Future Improvements

- Add support for more sensors and devices.
- Integrate voice control with platforms like Alexa or Google Assistant.
- Enable remote access and notifications via mobile apps.



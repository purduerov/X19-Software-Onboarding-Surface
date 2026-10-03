from src.zmq.python.messaging import Subscriber
from src.zmq.protocols.python import onboard_pb2
import socketio
import json
import time

sio = socketio.Client()
while True:
    try:
        sio.connect("http://127.0.0.1:5013")
        break
    except socketio.exceptions.ConnectionError:
        print("retrying")
        time.sleep(1)
        

def telemetry_callback(data):
    if sio.connected:
        sio.emit("depth", json.dumps({"data": data.depth}))
        sio.emit("temp", json.dumps({"data": data.temp}))
    print(f"Received depth: {data.depth} m, temp: {data.temp} C")

# Initialize subscriber (connects to address by default)
subscriber = Subscriber(
    address="tcp://127.0.0.1:5555",
    topic="depth_temp",
    message_type=onboard_pb2.DepthTemp,
    callback=telemetry_callback
)

# Process incoming messages in a loop
try:
    while True:
        subscriber.spin_once(timeout_ms=100000)
except KeyboardInterrupt:
        subscriber.close()

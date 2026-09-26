from src.zmq.protocols.python import telemetry_pb2
from src.zmq.python.messaging import Subscriber
import socketio
import json
import time

time.sleep(5)
sio = socketio.Client()
sio.connect("http://127.0.0.1:5013")


def callback(message):
    if (sio.connected):
        sio.emit("depth", json.dumps({"data": message.depth}))
        sio.emit("temp", json.dumps({"data": message.temperature}))
    # print(f"Depth: {message.depth} | Temp: {message.temperature}")

def main():
    
    subscriber = Subscriber(
        address="tcp://127.0.0.1:5555",
        topic="telemetry",
        message_type=telemetry_pb2.telemetry,
        callback=callback
    )
    while True:
        subscriber.spin_once(1000)

if __name__ == "__main__":
    main()
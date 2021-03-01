import zmq
import env
import time

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(f"tcp://{env.APP_HOST}:{env.OBS_SOCKET_PORT}")
time.sleep(1)
socket.send_json({"data": True})
socket.close()


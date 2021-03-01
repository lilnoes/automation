import zmq
import env

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect(f"tcp://{env.APP_HOST}:{env.FLASK_SOCKET_PORT}")
socket.setsockopt(zmq.SUBSCRIBE, b"") #Add this to be able to receive message from pub
print("connected")


count = 1
while True:
    count += 1
    if count % 10 == 0:
        print("polling after 10 seconds")
    if socket.poll(1000) == zmq.POLLIN:
        msg = socket.recv_json()
        print("message received after polling", msg)



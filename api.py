from slack import WebClient
from flask import Blueprint, request as req, current_app as app
import slackUtils as utils
import json
from datetime import datetime
import requests as r
import zmq
import env
import time

context = zmq.Context()
socket = context.socket(zmq.PUB)


api = Blueprint("api", __name__)

@api.route("/sendMessage")
def sendMessage():
	socket.bind(f"tcp://{env.APP_HOST}:{env.FLASK_SOCKET_PORT}")
	time.sleep(0.5) #sleep so that pub can be prepared
	socket.send_json({"time": datetime.now().timestamp()})
	print("send message successfully")
	socket.unbind(f"tcp://{env.APP_HOST}:{env.FLASK_SOCKET_PORT}")
	return {"text": "done"}

@api.route("/message")
def getMessage():
	response = {count: 0, link: ""}
	if len(app.config['links']) > 0:
		response[count] = 1
		response[link] = app.config['links'].pop()
	return response
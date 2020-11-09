from slack import WebClient
from flask import Blueprint, request as req, current_app as app
import slackUtils as utils
import json
from datetime import datetime
import requests as r

api = Blueprint("api", __name__)

@api.route("/getLink")
def getLink():
	response = {"count": 0, "link": None}
	if len(app.config['links']) > 0:
		response["count"] = 1
		response["link"] = app.config['links'][-1]
	return response

@api.route("/message")
def getMessage():
	response = {count: 0, link: ""}
	if len(app.config['links']) > 0:
		response[count] = 1
		response[link] = app.config['links'].pop()
	return response
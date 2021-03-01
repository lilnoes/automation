from slack import WebClient
from flask import Blueprint, request as req, current_app as app
import slackUtils
import json
from datetime import datetime
import requests as r
import subprocess

slackApi = Blueprint("slackApi", __name__)

@slackApi.route("/sendScreenshot", methods=["POST"])
def sendScreenshot():
	print("send screenshot command recieved")
	slackUtils.sendScreenshot()
	return f'OBS is {app.config["obs"]["status"]}'

@slackApi.route("/getstatus", methods=["POST"])
def getStatus():
	print(req.form)
	app.config["flask"]["time"] = datetime.now().timestamp()
	app.config["flask"]["command"] = "status"
	app.config["flask"]["response_url"] = req.form["response_url"]
	return f'OBS is {app.config["obs"]["status"]}'

@slackApi.route("/startrecord", methods=["POST"])
def startRecording():
	print(req.form)
	app.config["flask"]["time"] = datetime.now().timestamp()
	app.config["flask"]["command"] = "startrecord"
	app.config["flask"]["param"] = req.form["text"]
	return f'wait for some time...'

@slackApi.route("/stoprecord", methods=["POST"])
def stopRecording():
	print(req.form)
	app.config["flask"]["time"] = datetime.now().timestamp()
	app.config["flask"]["command"] = "stoprecord"
	app.config["flask"]["param"] = "zoom"
	return f'stopped recording successfully'
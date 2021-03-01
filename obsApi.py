from slack import WebClient
from flask import Blueprint, request as req, current_app as app
import slackUtils as utils
import json
from datetime import datetime
import requests as r
import subprocess

response_url = ""

obsApi = Blueprint("obsApi", __name__)

@obsApi.route("/getcommand", methods=["POST", "GET"])
def getCommand():
    return app.config["flask"]

@obsApi.route("/setStatus", methods=["POST", "GET"])
def setStatus():
    status = req.form["status"]
    app.config["obs"]["status"] = status
    print("new status", app.config["obs"])
    return app.config["obs"]
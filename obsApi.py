from slack import WebClient
from flask import Blueprint, request as req, current_app as app
import slackUtils as utils
import json
from datetime import datetime
import requests as r
import subprocess

obsApi = Blueprint("obsApi", __name__)

@obsApi.route("/getcommand", methods=["POST", "GET"])
def getCommand():
    return app.config["flask"]


@obsApi.route("/setStatus", methods=["POST", "GET"])
def setStatus():
    time = req.form["time"]
    status = req.form["status"]
    if time == app.config["obs"]["time"]:
        return app.config["obs"]
    app.config["obs"]["time"] = time
    app.config["obs"]["status"] = status
    return app.config["obs"]
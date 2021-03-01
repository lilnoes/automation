import obspython as obs
from datetime import datetime
import requests as r
import obsUtil
from traceback import print_exc as unwind
import env
from datetime import datetime
import time


_obs = {"time": datetime.now().timestamp(), "command": "status", "param": "param", "status": "OFFLINE"}
flask = {"time": datetime.now().timestamp(), "command": "status", "param": "param", "response_url": "response"}

def setStatus(status="STARTED"):
	if obs.obs_frontend_recording_active():
		status = "RECORDING"
	_obs["status"] = status
	_obs["time"] = datetime.now().timestamp()
	try:
		r.post("http://127.0.0.1:5000/obsApi/setStatus", data=_obs)
	except:
		pass

def getCommand():
	global flask
	try:
		response = r.post("http://127.0.0.1:5000/obsApi/getcommand", data=flask).json()
	except:
		return
	if flask["time"] == response["time"]:
		return

	flask = response
	command = flask["command"]
	if command == "startrecord":
		resp = obsUtil.startZoom(flask["param"])
		print("response", resp)
		if resp is None:
			# obsUtil.killZoom()
			setStatus("FAILED")
			return
		obsUtil.updateSource(resp[2])
		print("name", resp)
		setStatus("RECORDING")
	elif command == "stoprecord":
		obsUtil.killZoom()
		setStatus()

	elif command == "status" and obs.obs_frontend_recording_active():
		setStatus("RECORDING")
		print("going to take picture")
		d = obs.obs_frontend_take_screenshot()
		print("picture", d)
		try:
			r.post("http://127.0.0.1:5000/slack/sendScreenshot", timeout=1)
		except:
			pass

	elif command == "status":
		setStatus()

def update():
	getCommand()

def script_load(settings):
	setStatus()
	obs.timer_add(update, 1000)
	print("loaded at", datetime.now())

def script_unload():
	print("unloaded at", datetime.now())
	setStatus("OFFLINE")
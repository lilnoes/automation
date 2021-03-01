import obspython as obs
import sys
from datetime import datetime, timedelta
import requests as r
# import obsUtil as util
import time
from subprocess import run
import re
from traceback import print_exc as unwind
import env
import sys
from datetime import datetime
print("version", sys.version, sys.path)


_obs = {"time": datetime.now().timestamp(), "command": "status", "param": "param", "status": "OFFLINE"}
flask = {"time": datetime.now().timestamp(), "command": "status", "param": "param"}

def setStatus(status="STARTED"):
	if obs.obs_frontend_recording_active():
		status = "RECORDING"
	_obs["status"] = status
	r.post("http://127.0.0.1:5000/obsApi/setStatus", data=_obs)

def getCommand():
	global flask
	try:
		response = r.post("http://127.0.0.1:5000/obsApi/getcommand", data=flask).json()
	except:
		return
	if flask["time"] != response["time"]:
		flask = response
		print("code received", flask["command"])

def update():
	getCommand()

def script_load(settings):
	setStatus()
	obs.timer_add(update, 1000)
	obs.timer_add(setStatus, 1000*60)
	print("loaded Here at", datetime.now())

def script_unload():
	print("unloaded")


def startZoom(link):
	pid = newZoom(link[0])
	if pid is None:
		time.sleep(10)
	pid = newZoom(link[0])
	if pid is None:
		return False
	zm = ""
	print(pid, "all")
	for i in pid:
		if "Meeting" not in i[2]:
			zm = i
	pid = zm
	print(pid, "k")

	source = obs.obs_get_source_by_name("Window Capture (Xcomposite)")
	props = obs.obs_source_get_settings(source)
	print(pid, "here")
	capture = rf"{pid[1]}\r\nZoom\r\nzoom"
	obs.obs_data_set_string(props, "capture_window", capture)
	obs.obs_source_update(source, props)
	# json = obs.obs_data_get_json(props)
	obs.obs_source_release(source)
	return True

url = "https://istanbul-edu-tr.zoom.us/j/98555862270?pwd=Z2RXemRYZnh1VHpMVjNQSHd5UEt4Zz09&uname=LEON+EMMANUEL+ISHIMWE#success"

# newZoom(url)



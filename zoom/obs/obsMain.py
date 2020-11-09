import obspython as obs
import sys
from datetime import datetime, timedelta
import requests as r
import obsUtil as util
import time
from subprocess import run
import re
from traceback import print_exc as unwind

recording = False
activeLink = None
toSend = "http://localhost:5000"
notified = False


def getLink():
	try:
		response = r.get(f'{toSend}/api/getLink')
		if response.json().get("link"):
			return response.json().get("link")
	except:
		print(f"error 1{datetime.now()}")
		unwind()
		return None

def send(data):
	try:
		response = r.post(f'{toSend}/api/message', json=data)
		return response.text
	except:
		print(f"error {datetime.now()}")
		unwind()
		return None


def update():
	global recording
	global activeLink
	try:
		recording = obs.obs_frontend_recording_active()
		if recording:
			print("duh1")
			diff = (activeLink[2] - datetime.now()).total_seconds
			print("duh")
			if diff < 0 :
				obs.obs_frontend_recording_stop()
				send({"ok": f"stopped recording at {datetime.now()}"})
			return
		link = getLink()

		if link:
			print(link)
			print("started")
			startZoom(link)
			print("started1")
			obs.obs_frontend_recording_start()
			obs.obs_frontend_take_screenshot()
			link[1] = datetime.fromtimestamp(link[1])
			link[2] = datetime.fromtimestamp(link[2])
			activeLink = link
			send({"ok": f"recording started at {datetime.now()}"})

	except:
		print(f"error {datetime.now()}")
		unwind()


def script_load(settings):
	update()
	# obs.timer_add(update, 1000)
	print("loaded Here at", datetime.now())
	# try:
	# 	source = obs.obs_get_source_by_name("Window Capture (Xcomposite)")
	# 	name = obs.obs_source_get_name(source)
	# 	props = obs.obs_source_get_settings(source)
	# 		# obs.obs_data_set_string(props, "capture_window", "56623121\r\nZoom Cloud Meetings\r\nzoom")
	# 		# obs.obs_source_update(source, props)
	# 	json = obs.obs_data_get_json(props)
	# 	print(json)
	# 	obs.obs_source_release(source)
	# except:
	# 	print("failed", sys.exc_info())
	# print("finished")

def script_unload():
	print("unloaded")

def getDetails(filter="zoom.zoom"):
	output = run(f"wmctrl -lpx | grep {filter}", capture_output=True, encoding="utf-8", shell=True)
	outs = []
	for i in output.stdout.split("\n"):
		m = re.search(r"(.+?) +(.+?) +(.+?) +(.+?) +(.+?) (.+)", i, re.I)
		if m is None or len(m.groups())!=6:
			continue
		outs.append( (m.group(3), int(m.group(1), 16), m.group(6)) )
	return outs

def newZoom(url):
	for pid,_,_ in getDetails():
		run(f"kill -9 {pid}", shell=True)
	run(f"zoom --url={url}&", shell=True)
	print(url)
	time.sleep(10)
	pid = getDetails()
	if len(pid) > 0:
		return pid
	return None

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



from datetime import datetime, timedelta
from slack import WebClient
import slackViews as views
import env
import subprocess
import time

TOKEN = env.TOKEN

client = WebClient(token=TOKEN)

def sendScreenshot():
	print("before sleeping")
	time.sleep(5)
	print("after sleeping")
	d = subprocess.run("ls -t /home/leon | grep '.png'", capture_output=True, shell=True, encoding="utf-8")
	print(d.stdout.split("\n"))
	d = d.stdout.split("\n")[0]
	if len(d) < 6:
		return
	file = fr"/home/leon/{d}"
	client.files_upload(channels="#zoom", file=file, title=d)
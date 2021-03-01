import requests as r
import subprocess
from datetime import datetime
import re
import time
import obspython as obs


def killZoom():
    obs.obs_frontend_recording_stop()
    d = subprocess.run('wmctrl -lpx | grep "zoom.zoom"',
                       shell=True, capture_output=True, encoding="utf-8")
    pids = d.stdout.split("\n")
    for pid in pids:
        if len(pid) <= 5:
            continue
        s = pid.split()[2]
        subprocess.run(f'kill -9 {s}', shell=True)


def getName():
    d = subprocess.run('wmctrl -lp | grep "Zoom Meeting"',
                       shell=True, capture_output=True, encoding="utf-8")
    print("getname", d.stdout)
    pid = d.stdout.split("\n")[0]
    if len(pid) <= 5:
        return None
    pid = pid.split()
    hnd = pid[0]
    pid = pid[2]
    return (hnd, pid, f"{int(hnd, 16)}\r\nZoom Meeting\r\nzoom")


def startZoom(link, name="EMMA"):
    killZoom()
    link = re.sub(r"&.*", f"", link)  # Basic harmful code injection avoidance
    # Removing success in url
    link = re.sub(r"#success.*", f"&uname={name}", link)
    subprocess.run(f'zoom --url={link}&', shell=True)
    d = datetime.now()
    print("before time", d)
    time.sleep(15)
    print("after time", datetime.now())
    print("elapsed", (datetime.now()-d).total_seconds() )
    return getName()


def updateSource(capture):
    source = obs.obs_get_source_by_name("Window Capture (Xcomposite)")
    props = obs.obs_source_get_settings(source)
    obs.obs_data_set_string(props, "capture_window", capture)
    obs.obs_source_update(source, props)
    obs.obs_source_release(source)
    obs.obs_frontend_recording_start()

print(getName())
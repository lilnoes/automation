from slack import WebClient
from flask import Blueprint, request as req, current_app as app
import slackUtils as utils
import json
from datetime import datetime
import requests as r

response_url = ""

slackApi = Blueprint("slackApi", __name__)

@slackApi.route("/input", methods=["POST"])
def response():
	payload = json.loads(req.form.get("payload", ""))
	if payload.get("type", "") == "view_submission":
		view_id = payload["view"]["id"]
		values = payload["view"]["state"]["values"]
		join_url = values["join_url"]["join_url"]["value"]
		start_date = values["start_date"]["start_date"]["selected_date"]
		start_time = values["start_time"]["start_time"]["selected_time"]
		end_date = values["end_date"]["end_date"]["selected_date"]
		end_time = values["end_time"]["end_time"]["selected_time"]

		start_date = datetime.fromisoformat(f"{start_date}T{start_time}")
		end_date = datetime.fromisoformat(f"{end_date}T{end_time}")

		if(end_date <= start_date):
			view = utils.views.getHomeViewError("Error: *END TIME IS INVALID*")
			return {
				"response_action": "update",
				"view": view
			}
		else:
			d = r.post(response_url, json={"text": "We will inform you when starting recording"})
			app.config['links'].append((join_url, start_date.timestamp(), end_date.timestamp()))
			print(response_url, d.text)

	return ""

@slackApi.route("/record", methods=["POST"])
def shortcut():
	trigger_id = req.form.get("trigger_id")
	global response_url
	response_url = req.form.get("response_url")
	# print(response_url)
	view = utils.views.getHomeView("modal")
	d = utils.client.views_open(token=utils.TOKEN, view=view, trigger_id=trigger_id)
	return ""
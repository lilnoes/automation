from datetime import datetime, timedelta
from slack import WebClient
import slackViews as views
import ENV

TOKEN = ENV.TOKEN

client = WebClient(token=TOKEN)

def getDivider():
	return 		{"type": "divider"}


def getText(text, type="plain_text"):
	return {
		"type": type,
		"text": text
	}


def getHeaderBlock(text):
	return {
		"type": "header",
		"text": getText(text)
	}

def getInput(action_id):
	return {
		"type": "plain_text_input",
		"action_id": action_id
	}


def getInputBlock(text, action_id):
	return {
		"type": "input",
		"element": getInput(action_id),
		"label": getText(text),
		"block_id": action_id
	}

def getInputDate(action_id, date_type="date"):
	if action_id is None:
		return {}
	now = datetime.now()
	if "end" in action_id:
		now += timedelta(minutes=40)
		
	time = now.strftime("%H:%M")
	date = now.strftime("%Y-%m-%d")


	time = time if date_type == "time" else date

	return {
		"type": f"{date_type}picker",
		f"initial_{date_type}": time,
		"action_id": f'{action_id}'
	}

def getSection(text, action_id, date_type="date"):
	r = {
		"type": "section",
		"text": getText(text, "mrkdwn"),
		"accessory": getInputDate(action_id, date_type),
		"block_id": action_id or "a"
	}

	return {key: value for (key, value) in r.items() if action_id!=None or key!="accessory"}



def getButton(text, action_id, style="primary"):
	return {
		"type": "button",
		"text": getText(text),
		"action_id": action_id,
		"style": style
	}

def getButtonAction(text, action_id, style="primary"):
	return 		{
			"type": "actions",
			"elements": [
				getButton(text, action_id, style)
			]
		}


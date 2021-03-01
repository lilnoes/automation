import slackUtils as utils

def getHomeView(type="modal"):
	return {
		"type": type,
		"title": utils.getText("Zoom meeting"),
		"submit": utils.getText("Create"),
		"clear_on_close": True,
		"blocks": [
			utils.getHeaderBlock("New Meeting"),
			utils.getInputBlock("Join url", "join_url"),
			utils.getSection("Start date", "start_date", "date"),
			utils.getSection("Start time", "start_time", "time"),
			utils.getDivider(),
			utils.getSection("End date", "end_date", "date"),
			utils.getSection("End time", "end_time", "time"),
		]
	}

def getHomeViewError(error, type="modal"):
	return {
		"type": type,
		"title": utils.getText("Zoom meeting"),
		"submit": utils.getText("Create"),
		"blocks": [
			utils.getHeaderBlock("New Meeting"),
			utils.getInputBlock("Join url", "join_url"),
			utils.getSection("Start date", "start_date", "date"),
			utils.getSection("Start time", "start_time", "time"),
			utils.getDivider(),
			utils.getSection("End date", "end_date", "date"),
			utils.getSection("End time", "end_time", "time"),
			utils.getDivider(),
			utils.getSection(error, None)
		]
	}

def getHomeViewUpdated(type="modal"):
	r = {
		"type": type,
		"title": utils.getText("Zoom meeting"),
		"blocks": [
			utils.getHeaderBlock("Info"),
			utils.getSection("Thank you for believing in us...", None)
		]
	}
	# return {key: value for (key, value) in r.items() if }
	return r


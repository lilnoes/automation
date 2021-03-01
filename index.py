from flask import Flask, request as req
from slackApi import slackApi
from datetime import datetime
from obsApi import obsApi
import env



app = Flask(__name__)

app.config["obs"] = {"time": datetime.now().timestamp(), "command": "status", "param": "param", "status": "OFFLINE"}
app.config["flask"] = {"time": datetime.now().timestamp(), "command": "status", "param": "param", "response_url": "response"}


app.register_blueprint(slackApi, url_prefix="/slack")
app.register_blueprint(obsApi, url_prefix="/obsApi")

@app.route("/<path:path>")
def error(path):
	return "err"


app.run(port=env.APP_PORT, debug=True)

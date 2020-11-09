from flask import Flask, request as req
from slackApi import slackApi
from api import api

app = Flask(__name__)

app.config['links'] = []

app.register_blueprint(slackApi, url_prefix="/slack")
app.register_blueprint(api, url_prefix="/api")

@app.route("/<path:path>")
def error(path):
	print(app.config["links"])
	return "err"


app.run(port=5000, debug=True)

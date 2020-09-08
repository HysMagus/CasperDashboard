from flask import Flask
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from bs4 import BeautifulSoup, SoupStrainer
from flask_prometheus_metrics import register_metrics
import casperlabs_client
import json
import requests

statusurl = "http://34.68.157.85:40403/status"
r = requests.get(statusurl)
json = r.json()
peers = json["checklist"]["peers"]["details"]["count"]
strpeers = str(peers)
blockcount = json["checklist"]["lastFinalizedBlock"]["details"]["jRank"]
strblockcount = str(blockcount)
client = casperlabs_client.CasperLabsClient('deploy.casperlabs.io', 40401)

app = Flask(__name__)

@app.route("/")
def index():
    return "Test"
@app.route("/peers")
def peers():
    return strpeers
@app.route("/status")
def status():
  return json
@app.route("/blockcount")
def blockcount():
  return strblockcount

  

# provide app's version and deploy environment/config name to set a gauge metric
register_metrics(app, app_version="v0.1.2", app_config="staging")

# Plug metrics WSGI app to your main app with dispatcher
dispatcher = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})

run_simple(hostname="0.0.0.0", port=5000, application=dispatcher)


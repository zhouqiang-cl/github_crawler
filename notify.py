# -*- coding: utf-8 -*-
import json
import tornado.httpclient
from settings import NOTIFY_URL

def notify_as_link(repo):
    if not repo["description"] or repo["description"] == "":
        repo["description"] = "No description"
    title = repo["url"].split("/")[-1]
    text = u"star: " + str(repo["stars"]).decode("utf-8") + u"  forks: " + str(repo["forks"]).decode("utf-8") +u" description: " + repo["description"]
    data = {
        "msgtype": "link",
        "link": {
            "title": title,
            "text": text,
            "picUrl": "",
            "messageUrl": repo["url"]
        }
    }
    headers = {'Content-Type': 'application/json'}
    client = tornado.httpclient.HTTPClient()
    client.fetch(NOTIFY_URL, method="POST", body=json.dumps(data), headers=headers)

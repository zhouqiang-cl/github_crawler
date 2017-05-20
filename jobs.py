# -*- coding: utf-8 -*-
import json
import tornado.httpclient
import notify
from cron import CronTab
from timer import Cronjob, cron_set
from tornado.ioloop import IOLoop

class Job(object):

    def __init__(self, cron_time=None, job=None, description=""):
        self._cron_time = cron_time
        self._job = job
        self._schedule_time = None
        self._scheduled_time = 0
        self._description = description

def fetch_random_repo():
    url = "http://zhouqiang.site/api/v1/repos?count=1&lang=Python"
    repo = json.loads(synchronous_fetch(url))[0]
    notify.notify_as_link(repo)

def synchronous_fetch(url):
    http_client = tornado.httpclient.HTTPClient()
    response = http_client.fetch(url)
    return response.body


def main():
    entry = CronTab('30 0 * * *')
    c = Job(entry, fetch_random_repo, "fetch repo")
    cron_set.add(c)
    Cronjob(1000).start()
    IOLoop.instance().start()

if __name__ == "__main__":
    main()


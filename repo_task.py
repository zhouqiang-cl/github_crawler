# -*- coding: utf-8 -*-
import random
import Queue
import json
import time

import tornado.gen
import tornado.web
import tornado.httpclient
from tornado.ioloop import IOLoop, PeriodicCallback

import repos
from logger import gen_log
from settings import *

user_repos = set()
task_queue = Queue.Queue()


def get_famous_users(users_url):
    try:
        return [item[0] for item in json.loads(synchronous_fetch(users_url))]
    except Exception as e:
        print str(e)
        return []


def synchronous_fetch(url):
    http_client = tornado.httpclient.HTTPClient()
    response = http_client.fetch(url)
    return response.body


class Tasks(PeriodicCallback):
    """docstring for ClassName"""

    def __init__(self, callback_time):
        self._serving = False
        self._last_scan = 0
        super(Tasks, self).__init__(self.serve_loop, callback_time)

    def serve_loop(self):
        if self._serving:
            return
        self._serving = True
        try:
            try:
                url = task_queue.get_nowait()
                self.process_url(url["url"])
            except Queue.Empty:
                if time.time() - self._last_scan > 600:
                    famous_users = get_famous_users(FAMOUS_USERS)
                for uid in famous_users:
                    url = URL_PREFIX + 'users/' + uid \
                        + '/repos?access_token=' + ACCESS_TOKEN
                    task_queue.put({"url": url})
                    url = URL_PREFIX + 'users/' + uid \
                        + '/starred?access_token=' + ACCESS_TOKEN
                    task_queue.put({"url": url})
                if famous_users:
                    self._last_scan = time.time()
        finally:
            self._serving = False

    @tornado.gen.coroutine
    def process_url(self, url):
        try:
            print "process url..", url
            http_client = tornado.httpclient.AsyncHTTPClient(
                defaults=dict(user_agent="commit"))
            response = yield http_client.fetch(tornado.httpclient.HTTPRequest(
                url, connect_timeout=5, request_timeout=20))
            rs = repos.get_repos(json.loads(response.body))
            rs_dict = {}
            for r in rs:
                rs_dict[r.url] = r
            ur_dict = {}
            now = time.time()
            for r in user_repos:
                if now - r.update_time < 3600:
                    ur_dict[r.url] = r
            new_dict = {}
            new_dict.update(ur_dict)
            new_dict.update(rs_dict)
            user_repos.clear()
            user_repos.update(new_dict.values())
        except Exception as e:
            print str(e)
            pass


class ReposHandler(tornado.web.RequestHandler):

    def get(self):
        count = int(self.get_argument("count", 100))
        sort = self.get_argument("sort", False)
        lang = self.get_argument("lang", None)
        ur = [r for r in user_repos if not lang or r.lang == lang]
        if len(ur) < count:
            rs = [r.as_dict() for r in ur]
        else:
            rs = [r.as_dict() for r in random.sample(ur, count) if not sort] or [r.as_dict(
            ) for r in sorted(ur, key=lambda count:count.stars, reverse=True)[0:count]]
        self.finish(json.dumps(rs))


def make_app():
    return tornado.web.Application([
        (r"/api/v1/repos", ReposHandler),
    ],
    )

if __name__ == "__main__":
    Tasks(1000).start()
    app = make_app()
    app.listen(8889, address='127.0.0.1')
    IOLoop.instance().start()

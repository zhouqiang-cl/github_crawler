# -*- coding: utf-8 -*-

import json
import time
import Queue
import tornado.gen
import tornado.web
import tornado.httpclient
from tornado.ioloop import IOLoop, PeriodicCallback
from logger import gen_log
from settings import *
from collections import Counter

user_count = Counter()
ret_code = Counter()

user_new_set = set(["sardaukar"])
user_done_set = set()
task_queue = Queue.Queue()

def constract_fetch_following_url(uid):
    url = URL_PREFIX + 'users/' + uid \
        + '/following?access_token=' + ACCESS_TOKEN
    return url

def get_users(user_info):
    return [ info["login"] for info in user_info ]

class Tasks(PeriodicCallback):
    """docstring for ClassName"""

    def __init__(self, callback_time):
        self._serving = False
        super(Tasks, self).__init__(self.serve_loop, callback_time)

    def serve_loop(self):
        if self._serving:
            return
        self._serving = True
        try:
            url = task_queue.get_nowait()
            self.process_url(url)
        except Queue.Empty:
            for uid in user_new_set - user_done_set:
                url = constract_fetch_following_url(uid)
                task_queue.put({"url": url,"retry": 3})
                user_done_set.update(user_new_set)
                user_new_set.clear()
        finally:
            self._serving = False

    @tornado.gen.coroutine
    def process_url(self, url):
        try:
            gen_log.info("request..." + url["url"])
            if "retry" not in url:
                url["retry"] = 3
            http_client = tornado.httpclient.AsyncHTTPClient(
                defaults=dict(user_agent="commit"))
            response = yield http_client.fetch(tornado.httpclient.HTTPRequest(
                url["url"], connect_timeout=5, request_timeout=20))
            uids = get_users(json.loads(response.body))
            for uid in uids:
                user_count[uid] += 1
            user_new_set.update(uids)
            if "count" not in url or url["count"] == True:
                ret_code[200] += 1
        except tornado.httpclient.HTTPError as e:
            if e.code != 403:
                if "count" not in url or url["count"] == True:
                    ret_code[e.code] += 1
                if url["retry"] > 0:
                    url["retry"] -= 1
            task_queue.put(url)
            gen_log.info(str(e.code) + " " + url["url"])
        except Exception as e:
            if url["retry"] > 0:
                url["retry"] -= 1
                task_queue.put(url)
            gen_log.info(str(e) + " " + url["url"])

class UserHandler(tornado.web.RequestHandler):
    def get(self):
        count = int(self.get_argument("count",100))
        users = user_count.most_common(count)
        self.finish(json.dumps(users))

class StatusHandler(tornado.web.RequestHandler):
    def get(self):
        self.finish(json.dumps(ret_code))

def make_app():
    return tornado.web.Application([
        (r"/api/v1/users", UserHandler),
        (r"/status", StatusHandler),
    ],
    )

if __name__ == "__main__":
    Tasks(1000).start()
    app = make_app()
    app.listen(8888, address='127.0.0.1')
    IOLoop.instance().start()

import time
import json
import tornado.httpclient
import notify
from tornado.ioloop import IOLoop, PeriodicCallback

cron_set = set()


class Cronjob(PeriodicCallback):

    def __init__(self, callback_time):
        self._serving = False
        self._cocurrents = 0
        self._user_total_count = 0
        self._request_count = 0
        self.io_loop = IOLoop.current()

        super(Cronjob, self).__init__(self.register_loop, callback_time)

    def add_timeout(self, cron):
        print "add timeout at %s run %s" % (cron._schedule_time, cron._description)
        self.io_loop.add_timeout(cron._schedule_time, cron._job)

    def remove_timeout(self):
        pass

    def register_loop(self):
        now = time.time()
        new_cron_set = set()
        for cron in cron_set:
            if not cron._schedule_time:
                cron._schedule_time = cron._cron_time.next(
                    delta=False, default_utc=True)
            if cron._schedule_time < now + 120 and cron._scheduled_time != cron._schedule_time:
                cron_set.remove(cron)
                self.add_timeout(cron)
                cron._scheduled_time = cron._schedule_time
                cron._schedule_time = cron._cron_time.next(
                    now=cron._schedule_time, delta=False, default_utc=True)
                cron_set.add(cron)

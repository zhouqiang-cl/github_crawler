# -*- coding: utf-8 -*-
import time
from filter import Filter
class Repo(object):

    def __init__(self, url=None, stars=0, forks=0, description="",lang=None, update_time=None):
        self.url = url
        self.stars = stars
        self.forks = forks
        self.description = description
        self.lang = lang
        self.update_time = update_time

    def as_dict(self, *args):
        d = self.__dict__
        if args:
            return dict((k, getattr(self, k)) for k in args)
        else:
            return dict((k, d[k]) for k in d.iterkeys() if not k.startswith("_"))

def get_repos(repos_info):
    f = Filter()
    # f.add_filter(lambda repo: repo["fork"] == False)
    f.add_filter(lambda repo: repo["language"] in ["Python","JavaScript","C","Go"])
    f.add_filter(lambda repo: repo["stargazers_count"] > 500)
    repos = f.filter_repos(repos_info)
    rs = set()
    for repo in repos:
        stars = repo["stargazers_count"]
        forks = repo["forks"]
        url = repo["html_url"]
        description = repo["description"]
        lang = repo["language"]
        t = int(time.time())
        rs.add(Repo(url, stars, forks, description, lang, t))
    return rs

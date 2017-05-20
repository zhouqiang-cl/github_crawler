# -*- coding: utf-8 -*-
class Filter(object):

    def __init__(self):
        self.filters = set()

    def add_filter(self, f=None):
        if f:
            self.filters.add(f)

    def filter_repo(self, repo=None):
        if not repo:
            return None
        tmp_result = repo
        for f in self.filters:
            if f(tmp_result):
                continue
            else:
                return None
        return tmp_result

    def filter_repos(self, repos=None):
        if not repos:
            return []

        tmp_repos = repos
        for f in self.filters:
            tmp_repos = filter(f, tmp_repos)
        return tmp_repos

# github_crawler

用于抓取 github 上有名的用户的关注的repo

主要分为两个部分:
<br/>&emsp;&emsp;1.user_task.py 这个以某一个用户为起点，开始抓取他关注的人，添加到抓取列表中，对外输出关注人数最大的若干用户
<br/>&emsp;&emsp;2.repo_task.py 获取上一个程序抓取的有名的用户，抓取他们 star 和 自己创建的 repo(repo 通过过滤程序filter.py 过滤了，可自定义 filter)

我的 filter 是获取 star 数超过 500，并且语言是 Python, C, Go, Javascript 的

demo:
    <br/>&emsp;&emsp;[zhouqiang.site/api/v1/users](http://zhouqiang.site/api/v1/users)
    <br/>&emsp;&emsp;[zhouqiang.site/api/v1/users?count=10](http://zhouqiang.site/api/v1/users?count=10)
    <br/>&emsp;&emsp;[zhouqiang.site/api/v1/repos](http://zhouqiang.site/api/v1/repos)
    <br/>&emsp;&emsp;[zhouqiang.site/api/v1/repos?count=3](http://zhouqiang.site/api/v1/repos?count=3)

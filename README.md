# github_crawler

用于抓取 github 上有名的用户的关注的repo

主要分为几个部分:
<br/>&emsp;&emsp;1.repo_task_v2.py 通过抓取github search 的api，抓取关注的各语言排名最前的900个repo(repo 通过过滤程序filter.py 过滤了，可自定义 filter)
<br/>&emsp;&emsp;2.jobs.py 主要定时从 repos 里面随机获取一个 repo，并发送到钉钉群里

我的 filter 是获取 star 数超过 500，并且语言是 Python, C, Go, Javascript 的


repos 的 api 支持三个参数 count,lang,sort. 顾名思义,count 是最终显示多少个, lang 是显示哪个语言的, 如果不加sort,那随机取 repo

demo:
    <br/>&emsp;&emsp;[zhouqiang.site/api/v1/users](http://zhouqiang.site/api/v1/users)
    <br/>&emsp;&emsp;[zhouqiang.site/api/v1/users?count=10](http://zhouqiang.site/api/v1/users?count=10)
    <br/>&emsp;&emsp;[zhouqiang.site/api/v1/repos](http://zhouqiang.site/api/v1/repos)
    <br/>&emsp;&emsp;[zhouqiang.site/api/v1/repos?count=3](http://zhouqiang.site/api/v1/repos?count=3)
    <br/>&emsp;&emsp;[zhouqiang.site/api/v1/repos?count=3&lang=Python&sort=true](http://zhouqiang.site/api/v1/repos?count=3&lang=Python&sort=true)
    <br/>&emsp;&emsp;[zhouqiang.site/api/v2/repos](http://zhouqiang.site/api/v2/repos)
    <br/>&emsp;&emsp;[zhouqiang.site/api/v2/repos?count=3](http://zhouqiang.site/api/v2/repos?count=3)
    <br/>&emsp;&emsp;[zhouqiang.site/api/v2/repos?count=3&lang=Python&sort=true](http://zhouqiang.site/api/v2/repos?count=3&lang=Python&sort=true)

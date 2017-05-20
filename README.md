# github_crawler
用于抓取 github 上有名的用户的关注的repo
<br/>
主要分为两个部分:
<br/>
&emsp;&emsp;1.user_task.py 这个以某一个用户为起点，开始抓取他关注的人，添加到抓取列表中，对外输出关注人数最大的若干用户
&emsp;&emsp;2.repo_task.py 获取上一个程序抓取的有名的用户，抓取他们 star 和 自己创建的 repo(repo 通过过滤程序filter.py 过滤了，可自定义 filter)

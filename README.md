# pybilibili
一个简易的bilibili视频下载器。

实现了多清晰度视频和音频下载、合并。

目前引用了`requests,re,json,subprocess,BeautifulSoup`。

音视频合并过程采用了命令行调用ffmpeg的方式，因此需要正确安装ffmpeg并配置环境变量。

详细请见：
[Hlwdy's Blog](https://hlwdyblog.tk/2020/08/30/python%E4%B8%8B%E8%BD%BDbilibili%E8%A7%86%E9%A2%91/)
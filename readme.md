## Project Illustration ##

**工程说明：**
    一个多线程网页爬虫，用于动态、静态网页抓取，生成网站快照。配合chrome linkGrabber 链接提取插件使用。软件初衷是爬取知乎文章，理论可以快速抓取任何网站，生成网站快照。
    支持多线程，每个线程会在工程目录下生成"User Data[线程id]"的用户数据目录。保留用户的登录信息，填表信息等。

**使用说明：**
    Python环境3.xx;
    库依赖见requirement.txt
    使用pip3 install -r requirement.txt 一键安装所有依赖库
    其他依赖：谷歌浏览器，对应谷歌浏览器版本的ChromeDriver。
    对于需要登录的网站，可设ZhihuThread类实例化参数authenticate为True，authUrl设为登录网页链接，然后在弹出的浏览器中输入账号或扫码等方式进行登录。登录数据将保存到对应线程的“User Data” 目录。然后，authenticate参数设为False，重新运行开始自动抓取。
    要爬取的网页所有链接经Grabber link 插件提取后放进linklists数组中，如工程中所示。
    每个线程的意外错误日志会被记录到工程目录下log[线程号id].txt文档中。
    浏览器默认以无头方式工作。在登录时，为了方便用户登录，设为有头工作方式。




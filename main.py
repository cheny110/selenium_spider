from typing import List
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import time
from selenium.webdriver.chrome import options
from lxml import etree
from selenium.webdriver.common import desired_capabilities
from threading import Thread
import os

authUrl="https://zhuanlan.zhihu.com"
linklists=[
"https://zhuanlan.zhihu.com/p/414783403",
"https://zhuanlan.zhihu.com/p/414421797",
"https://zhuanlan.zhihu.com/p/414156317",
"https://zhuanlan.zhihu.com/p/413559890",
"https://zhuanlan.zhihu.com/p/413255204",
"https://zhuanlan.zhihu.com/p/412796439",
"https://zhuanlan.zhihu.com/p/412447787",
"https://zhuanlan.zhihu.com/p/412376561",
"https://zhuanlan.zhihu.com/p/412198397",
"https://zhuanlan.zhihu.com/p/411965359",
"https://zhuanlan.zhihu.com/p/411975330",
"https://zhuanlan.zhihu.com/p/411665546",
"https://zhuanlan.zhihu.com/p/411629045",
"https://zhuanlan.zhihu.com/p/411313621",
"https://zhuanlan.zhihu.com/p/411073943",
"https://zhuanlan.zhihu.com/p/410928122",
"https://zhuanlan.zhihu.com/p/410724745",
"https://zhuanlan.zhihu.com/p/410634693",
"https://zhuanlan.zhihu.com/p/410248031",
"https://zhuanlan.zhihu.com/p/409953480",
"https://zhuanlan.zhihu.com/p/409503873",
"https://zhuanlan.zhihu.com/p/409471061",
"https://zhuanlan.zhihu.com/p/409309037",
"https://zhuanlan.zhihu.com/p/409282781",
"https://zhuanlan.zhihu.com/p/409032725",
"https://zhuanlan.zhihu.com/p/409018432",
"https://zhuanlan.zhihu.com/p/408892371",
"https://zhuanlan.zhihu.com/p/408878363",
"https://zhuanlan.zhihu.com/p/408653857",
"https://zhuanlan.zhihu.com/p/408588717",
"https://zhuanlan.zhihu.com/p/408325943",
"https://zhuanlan.zhihu.com/p/408285852",
"https://zhuanlan.zhihu.com/p/407759449",
"https://zhuanlan.zhihu.com/p/407393884",
"https://zhuanlan.zhihu.com/p/407319755",
"https://zhuanlan.zhihu.com/p/407034531",
"https://zhuanlan.zhihu.com/p/407016891",
"https://zhuanlan.zhihu.com/p/406759424",
"https://zhuanlan.zhihu.com/p/406730426",
"https://zhuanlan.zhihu.com/p/406586522"
]
maxThread=3 #线程个数,不建议超过5个。如果需要登录，还受服务器会话保持数影响
targetdir=r"./pngs/"
#https://zhuanlan.zhihu.com/p/442154793



#print(zhihuDriver.page_source)


'''
with open("test.html","w")as f:
    f.write(zhihuDriver.page_source)
    f.close()
'''

class ZhihuThread(Thread):
    def __init__(self, id,linklist:List, authenticate:bool=False, group: None = ...):
        super().__init__(group=None)
        self.id=id
        self.linklist=linklist
        print("parser:",self.id,self.linklist)
        self.path=r"./User Data{}".format(self.id)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        chrome_options = webdriver.ChromeOptions()
        if not authenticate:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(r"user-data-dir="+self.path)
        self.browser=webdriver.Chrome(options=chrome_options)
        self.browser.set_page_load_timeout(300)
        self.browser.set_script_timeout(300)
        if authenticate:
            self.browser.get(authUrl)
        else:
            self.start()

        

    
    def run(self):
        for i in self.linklist:
            try:
                self.browser.get(i)
                width =self.browser.execute_script("return Math.max(document.body.scrollWidth, document.body.offsetWidth, document.documentElement.clientWidth, document.documentElement.scrollWidth, document.documentElement.offsetWidth);")
                height =self.browser.execute_script("return Math.max(document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")
                self.browser.set_window_size(width,height)
                self.html=etree.HTML(self.browser.page_source)
                self.browser.save_screenshot(targetdir+str(self.id*div+self.linklist.index(i))+self.html.xpath("//title")[0].text+".png")
            except Exception as e:
                with open("log{}.txt".format(self.id),"a")as f:
                    f.write("error:{}\n{}".format(i,e))
        self.browser.close() #关闭driver，避免内存溢出

#etree.HTML(zhihuDriver.page_source).xpath("//title")[0].text
if __name__=="__main__":
    if not os.path.exists(targetdir): #创建目标文件夹
        os.makedirs(targetdir)
    parsers=[]
    div=len(linklists)//min(maxThread,len(linklists))
    print("div:",div)
    for i in range(0,min(maxThread,len(linklists))):
        print(i)
        print("range:",i*div,min((i+1)*div-1,len(linklists)-1))
        print(linklists[i*div:min((i+1)*div-1,len(linklists)-1)])
        parsers.append(ZhihuThread(i,linklists[i*div:min((i+1)*div-1,len(linklists)-1)]))
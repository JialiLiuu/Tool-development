# encoding=utf8
from numpy import record
from selenium import webdriver
import time
import datetime
from threading import Thread,Lock
from PIL import Image
import pandas
from pandas.io.json import json_normalize

class showpng(Thread):
    def __init__(self, data):
        Thread.__init__(self)
        self.data = data

    def run(self):
        img = Image.open(self.data) 
        img.show()

class myThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
    # 前台开启浏览器模式
    def run(self):
        # 加启动配置
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
        # 不开浏览器
        option.add_argument("-headless")
        driver = webdriver.Chrome(chrome_options=option)
        driver.get("登录页面url")
        
        # 显示二维码
        driver.find_element_by_xpath("/html/body/div/div[1]/div/div[1]/a").click() 
        time.sleep(0.5)

        driver.get_screenshot_as_file("C:\\Users\\liujiali3\\Desktop\\DS\\code.png")
        t = showpng("code.png")
        t.start()
        time.sleep(13)
        global i
        global update_data
        lock.acquire()
        index = i
        i = i + 1
        lock.release()
        while index < end_index:
            headers = {}
            url = "修改页面url&taskId={}".format(data.loc[index]['taskId'])
            times = str(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
            task = Task(driver, url, data.loc[index]['new_scriptStartFile'], headers, times)
            print('脚本{}修改为{}'.format(data.loc[index]['old_scriptStartFile'], data.loc[index]['new_scriptStartFile']))
            back = {'taskId': data.loc[index]['taskId'], 'old_scriptStartFile': data.loc[index]['old_scriptStartFile'], 'new_scriptStartFile': data.loc[index]['new_scriptStartFile']}
            if task.updatePath():
                back['is_success'] = 1
                back['time'] = times
            else:
                back['is_success'] = 0
                back['time'] = times
            lock.acquire()
            print(index, self.name)
            print(back)
            update_data.append(back)
            index = i
            i = i + 1
            lock.release()
        if len(update_data) == end_index:
            print(update_data)
            df = json_normalize(update_data)
            writer = pandas.ExcelWriter('EXCEL\\迁移记录_多线程.xlsx')
            df.to_excel(writer, 'Sheet1')
            writer.save()

class Task():

    def __init__(self, driver, url, script_name, headers, times):
        '''
        初始化
        :param driver:驱动浏览器
        :param url:请求的路径
        :param script_name:更新的脚本名称
        :param headers:请求头
        :param times:请求发起的时间
        '''
        self.driver = driver
        self.url = url
        self.script = script_name
        self.headers = headers
        self.times = times

    def getScreen(self, target):
        '''
        屏幕截图
        :param target:迁移脚本是否成功标签（成功：target=1 失败:target=0）
        '''
        driver = self.driver
        name = self.url[-6:] + "_" + target + "_" + self.times
        path = "C:\\Users\\liujiali3\\Desktop\\DS\\SCREEN\\{}.png".format(name)
        driver.set_window_size(1263, 2226)
        driver.get_screenshot_as_file(path)
        
    def updatePath(self):
        '''
        更新路径
        '''
        try:
            driver = self.driver
            driver.get(self.url)

            driver.switch_to.frame("iFrameTaskEdit")
            driver.find_element_by_xpath("//*[@id='task-script-choose']").click()  
            time.sleep(0.1)

            elem = driver.find_element_by_id("scriptNameStr")
            elem.send_keys(self.script)
            # 搜索脚本
            driver.find_element_by_xpath("//*[@id='script-search-btn']").click()  
            time.sleep(3) 
            # 选中脚本
            is_content = driver.find_element_by_xpath("//*[@id='GridScriptCtrl']/div/div[3]/div[5]").text
            if is_content != '共0条':
                script_name_new = driver.find_element_by_xpath("//*[@id='gridScroller']/section/div/div/table/tbody/tr[1]/td[2]/div/span/span/div").text
                if self.script == script_name_new:
                    driver.find_element_by_xpath("//*[@id='gridScroller']/section/div/div/table/tbody/tr/td[1]/div/span/span/i[1]").click()
                else:
                    self.driver = driver
                    Task.getScreen(self, "0")
                    return False
            else:
                self.driver = driver
                Task.getScreen(self, "0")
                return False

            time.sleep(0.1)
            # 确定
            driver.find_element_by_xpath("//*[@id='script-save']").click()  
            self.driver = driver
            time.sleep(0.1)   
            
            # 提交修改
            driver.find_element_by_xpath("//*[@id='submit-btn']").click()
            time.sleep(0.1)
            Task.getScreen(self, "1")
            return True
        except Exception as e:
            return False

data = pandas.read_excel('EXCEL\\UPDATE_PATH.xlsx','Sheet10')
i = 0
end_index = len(data)
update_data = []
lock = Lock()
# 创建线程
threads = []
for a in range(1):
    name = 'Thread-' + str(a)
    threads.append(myThread(name))
for thread in threads:
    thread.start()
    time.sleep(8)
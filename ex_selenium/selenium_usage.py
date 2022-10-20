# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-19
# @file    : selenium_usage.py
# @function: Selenium模块的用法。
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ChromeOptions
import time


class BrowserCtrl:
    def __init__(self):
        """
        初始化浏览器对象
        """
        option = ChromeOptions()
        # 隐藏WebDriver提示条和自动化扩展信息
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)
        # 无头（Headless）模式：节省资源加载的时间和网络带宽
        option.add_argument('--headless')

        self.browser = webdriver.Chrome(options=option)
        # self.browser = webdriver.Firefox()
        # self.browser = webdriver.Safari()
        # self.browser = webdriver.Edge()

        # 反屏蔽（将window.navigator的webdriver属性置空）
        self.browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
        })


    def browser_get(self, url):
        """
        访问页面
        :param url
        :return:
        """
        self.browser.get(url)
        print(self.browser.page_source)  # 控制台输出淘宝页面的源代码
        print('='*32)
        # browser.close()

    def find_node(self, url):
        """
        查找节点
        注：在新版的Selenium中，find_element_by_xxx的方法已经弃用
        :param url
        :return:
        """
        self.browser_get(url)
        # 获取输入框对应的节点，各种获取方式返回结果一致
        input_1 = self.browser.find_element(by=By.ID, value='q')
        input_2 = self.browser.find_element(by=By.CSS_SELECTOR, value='#q')
        input_3 = self.browser.find_element(by=By.NAME, value='q')
        input_4 = self.browser.find_element(by=By.XPATH, value='//*[@id="q"]')
        print(input_1, input_2, input_3, input_4)
        print('-'*32)
        # 获取左侧导航条的所有条目（多个节点），返回值为列表，列表中每个节点均为WebElement类型
        lis = self.browser.find_elements(by=By.CSS_SELECTOR, value='.service-bd li')
        print(lis)
        print('='*32)

    def browser_interaction(self, url):
        """
        浏览器节点交互
        :param url
        :return:
        """
        self.browser_get(url)
        input_area = self.browser.find_element(By.ID, 'q')  # 找到输入框
        input_area.send_keys('Huawei')  # 输入文字
        time.sleep(1)
        input_area.clear()  # 清空输入框
        input_area.send_keys('李宁')
        button = self.browser.find_element(By.CLASS_NAME, 'btn-search')  # 找到搜索按钮
        button.click()  # 点击搜索按钮

    def browser_action_chain(self, url):
        """
        动作链
        针对无特定执行对象的交互，如鼠标拖拽、键盘按键等
        :param url
        :return:
        """
        self.browser_get(url)
        self.browser.switch_to.frame('iframeResult')
        source = self.browser.find_element(By.CSS_SELECTOR, '#draggable')
        target = self.browser.find_element(By.CSS_SELECTOR, '#droppable')
        actions = ActionChains(self.browser)
        actions.drag_and_drop(source, target)  # 声明拖拽对象和拖拽目标
        actions.perform()  # 执行动作

    def browser_js(self, url):
        """
        模拟运行JavaScript
        主要针对那些未提供API的功能。以下拉进度条为例
        :param url
        :return:
        """
        self.browser_get(url)
        self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        self.browser.execute_script('alert("To Bottom")')

    def get_node(self, url):
        """
        获取节点信息
        :param url
        :return:
        """
        self.browser_get(url)
        logo = self.browser.find_element(By.CLASS_NAME, 'logo-image')
        print(logo)
        print(logo.get_attribute('src'))  # 获取节点src属性
        input = self.browser.find_element(By.CLASS_NAME, 'logo-title')
        print(input.text)  # 获取节点text属性（节点内部文本信息）
        print(input.id)  # 获取节点ID
        print(input.location)  # 获取节点在页面中的相对位置
        print(input.tag_name)  # 获取标签名称
        print(input.size)  # 获取节点大小

    def change_frame(self, url):
        """
        切换Frame
        当页面中包含子Frame时，如果想获取子Frame中的节点，需要先调用switch_to.frame切换到对应的Frame再进行操作
        :param url:
        :return:
        """
        self.browser_get(url)
        self.browser.switch_to.frame('iframeResult')  # 切换到子Frame里
        try:
            logo = self.browser.find_element(By.CLASS_NAME, 'logo')
        except NoSuchElementException:
            print('NO LOGO')
        self.browser.switch_to.parent_frame()
        logo = self.browser.find_element(By.CLASS_NAME, 'logo')
        print(logo)

    def delay_implicit(self, url):
        """
        隐式等待：在查找DOM节点而节点没有立即出现时，先等待一段时间再查找
        在必要的时候，需要设置浏览器延时等待一段时间，确保节点已经加载出来
        :param url:
        :return:
        """
        self.browser.implicitly_wait(10)
        self.browser_get(url)
        input = self.browser.find_element(By.CLASS_NAME, 'logo-image')
        print(input)

    def delay_explicit(self, url):
        """
        显式等待：指定要查找的节点和最长等待时间
        :param url:
        :return:
        """
        self.browser_get(url)
        wait = WebDriverWait(self.browser, 10)
        input = wait.until(ec.presence_of_element_located((By.ID, 'q')))
        button = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search')))
        print(input, button)

    def back_and_forward(self, url1, url2, url3):
        """
        后退和前进操作
        :param url3:
        :param url2:
        :param url1:
        :return:
        """
        self.browser_get(url1)
        self.browser_get(url2)
        self.browser_get(url3)
        self.browser.back()
        time.sleep(1)
        self.browser.forward()

    def cookie(self, url):
        """
        操作cookie
        :param url:
        :return:
        """
        self.browser_get(url)
        print(self.browser.get_cookies())
        self.browser.add_cookie({'name': 'name', 'domain': 'www.zhihu.com', 'value': 'johnson'})
        print(self.browser.get_cookies())
        self.browser.delete_all_cookies()
        print(self.browser.get_cookies())

    def tab(self, url1, url2, url3):
        """
        选项卡管理
        :param url3:
        :param url2:
        :param url1:
        :return:
        """
        self.browser_get(url1)
        self.browser.execute_script('window.open()')
        print(self.browser.window_handles)
        self.browser.switch_to.window(self.browser.window_handles[1])
        self.browser_get(url2)
        time.sleep(1)
        self.browser.switch_to.window(self.browser.window_handles[0])
        self.browser_get(url3)

    def exception(self, url):
        """
        异常处理
        :return:
        """
        try:
            self.browser_get(url)
        except TimeoutException:
            print('Time Out')
        try:
            self.browser.find_element(By.ID, 'hello')
        except NoSuchElementException:
            print('No Element')
        finally:
            self.browser.close()

    def anti_block_test(self, url):
        """
        反屏蔽测试
        :param url:
        :return:
        """
        self.browser_get(url)

    def headless_test(self, url):
        """
        无头模式测试
        :param url:
        :return:
        """
        self.browser.set_window_size(1366, 768)  # 设置窗口的大小
        self.browser_get(url)
        self.browser.get_screenshot_as_file('preview.png')  # 输出页面截图


if __name__ == '__main__':
    browserCtrl = BrowserCtrl()
    # browserCtrl.find_node('https://www.taobao.com')
    # browserCtrl.browser_interaction('https://www.taobao.com')
    # browserCtrl.browser_action_chain('https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')
    # browserCtrl.browser_js('https://www.zhihu.com/explore')
    # browserCtrl.get_node('https://spa2.scrape.center/')
    # browserCtrl.change_frame('https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')
    # browserCtrl.delay_implicit('https://spa2.scrape.center/')
    # browserCtrl.delay_explicit('https://www.taobao.com')
    # browserCtrl.back_and_forward('https://www.baidu.com', 'https://www.taobao.com', 'https://www.python.org')
    # browserCtrl.cookie('https://www.zhihu.com/explore')
    # browserCtrl.tab('https://www.baidu.com', 'https://www.taobao.com', 'https://www.python.org')
    # browserCtrl.exception('https://www.baidu.com')
    # browserCtrl.anti_block_test('https://antispider1.scrape.center/')
    browserCtrl.headless_test('https://www.baidu.com')

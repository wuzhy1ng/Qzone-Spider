from selenium import webdriver
from util import getMsgList, getImgList, writeMsgList, writeImgList
import time
import os

print('---QQ空间小爬虫---')
print('-使用说明：')
print('-1、请确保您已登录QQ')
print('-2、该爬虫只允许爬取QQ好友')
print('-3、请确保您已安装chrome以及对应的chrome_driver')

pageIndex = 1
imgNumber = 1
qqNumber = input('输入爬取的好友QQ号：')
foldPath = './result/' + qqNumber
imgPath = foldPath + '/images'
textPath = foldPath + '/text'

browser = webdriver.Chrome()
browser.get('http://user.qzone.qq.com/' + qqNumber + '/311')

# 创建存档
if os.path.exists('result') is False:
    os.mkdir('./result')

if os.path.exists(foldPath) is False:
    os.mkdir(foldPath)

if os.path.exists(imgPath) is False:
    os.mkdir(imgPath)
    print('图像库创建中..')
print('图像库创建完成..')

if os.path.exists(textPath) is False:
    os.mkdir(textPath)
    with open(textPath + '/' + qqNumber + '.txt', 'w') as f:
        print('文档库创建中..')
print('文档库创建完成..')

# 进入验证身份
login_frame = browser.find_element_by_css_selector('#login_frame')
browser.switch_to.frame(login_frame)
browser.find_element_by_class_name('face').click()
browser.switch_to_default_content()
browser.implicitly_wait(10)

try:
    while True:
        browser.save_screenshot('temp.png')

        # 输出抓取页码
        print('正在抓取..第' + str(pageIndex) + '页说说')
        pageIndex += 1

        # 进入空间
        frame = browser.find_element_by_css_selector('.app_canvas_frame')
        browser.switch_to.frame(frame)

        # 获取说说列表--文字部分
        time.sleep(2.0)
        contexts = browser.find_elements_by_class_name('content')
        dates = browser.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')
        msgList = getMsgList(contexts, dates)
        writeMsgList(msgList, textPath)

        # 获取说说列表--图片部分
        time.sleep(2.0)
        imageAnchors = browser.find_elements_by_css_selector('[title=查看大图]')
        imgList = getImgList(imageAnchors)
        imgNumber = writeImgList(imgList, imgNumber, imgPath)

        time.sleep(2.0)
        # 切换到下一页
        browser.find_element_by_css_selector('[title=下一页]').click()
        browser.switch_to_default_content()
except Exception:
    print('爬取结束..')

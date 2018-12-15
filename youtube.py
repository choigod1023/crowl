import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import pymysql

db = pymysql.connect(host='127.0.0.1', port=3306, user='choigod1023',
                     passwd='jjang486', db='choigod1023', charset='utf8')
cursor = db.cursor()
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome('./chromedriver', chrome_options=options)
driver.get('https://www.youtube.com/results?sp=CAM%253D&search_query=%EC%95%84%EC%9D%B4%EC%A6%88%EC%9B%90+%EC%A7%81%EC%BA%A0+4k')
time.sleep(7)
a = driver.find_element_by_xpath('//*[@id="contents"]/ytd-video-renderer[20]')
ActionChains(driver).move_to_element(a).perform()
time.sleep(5)
a = driver.find_element_by_xpath('//*[@id="contents"]/ytd-video-renderer[40]')
ActionChains(driver).move_to_element(a).perform()
time.sleep(5)
a = driver.find_element_by_xpath('//*[@id="contents"]/ytd-video-renderer[60]')
ActionChains(driver).move_to_element(a).perform()
time.sleep(5)
for v in range(60, 161):
    a = driver.find_element_by_xpath('//*[@id="contents"]/ytd-video-renderer['+str(v)+']')
    ActionChains(driver).move_to_element(a).perform()
    time.sleep(5)
    v+=10
for i in range(57, 161):
    time.sleep(3)
    a = driver.find_element_by_xpath(
        '//*[@id="contents"]/ytd-video-renderer['+str(i)+']')
    ActionChains(driver).move_to_element(a).perform()
    a.click()
    time.sleep(5)
    source = driver.current_url
    os.system('youtube-dl -o '+"/home/choigod1023/izone/public/videos/hd/'(CAM)'"+str(i) +
              '.mp4 '+source+' -f 137+251')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    body = '(CAM)' + \
        soup.select('#container > h1 > yt-formatted-string')[0].get_text()
    print(body)
    sql = "INSERT INTO youtube(id,name) VALUES(%s, %s)"
    cursor.execute(sql, (i, body))
    db.commit()
    driver.execute_script('window.history.go(-1)')
    a = driver.find_element_by_xpath(
        '//*[@id="contents"]/ytd-video-renderer['+str(i)+']')
    ActionChains(driver).move_to_element(a).perform()

db.close()
driver.quit()

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome('/home/choigod1023/vlivecrowling/chromedriver', chrome_options=options)

driver.get('https://channels.vlive.tv/C1B7AF/video')
time.sleep(3)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
check = soup.find(class_="icon icon_live_onair")
try :
    onclick = driver.find_element_by_css_selector('#container > channel > div > video-list > div > div > ul > li.list_item.onair > video-list-item > div > a')
    onclick.click()
    time.sleep(1)
    url = driver.current_url
    url = url.replace("/video/","/embed/")
    url2 = url.split('?')
    url =url2[0]
    driver.quit()
except : 
    driver.find_element_by_xpath('//*[@id="container"]/channel/div/video-list/div/div/ul/li[1]/video-list-item/div/a').click()
    time.sleep(1)
    url = driver.current_url
    url = url.replace("/video/","/embed/")
    url2 = url.split('?')
    url =url2[0]
    driver.quit()
f = open("/home/choigod1023/izone/url.txt","w")
f.write(url)
f.close()

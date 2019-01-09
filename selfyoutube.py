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

i = 161
source_ = input("유튜브 주소를 입력하십시오 : ")
db = pymysql.connect(host='127.0.0.1', port=3306, user='choigod1023',
                     passwd='jjang486', db='choigod1023', charset='utf8')
cursor = db.cursor()
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome('./chromedriver', chrome_options=options)

naver = input('네이버tv라면 1 아니면 0을 눌러주세요: ')
ischeck = input('직캠이면 1, 아니면 0을 눌러주세요: ')

driver.get(source_)
time.sleep(5)

if int(naver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    source = soup.select('#clipInfoArea > div.watch_title > h3')[0].get_text()
    sql = 'select max(id) from youtube;'
    cursor.execute(sql)
    rows = cursor.fetchall()
    i = rows[0]
    i = int(i[0])+1
    print(i)
    try:
        os.system('youtube-dl -o '+"/home/choigod1023/izone/public/videos/hd/" +"'(CAM)"+str(i)+".mp4' "+source_+" -f AVC_1080P_1920_5120_192")
    except:
        os.system('youtube-dl -o '+"/home/choigod1023/izone/public/videos/hd/" +"'(CAM)"+str(i)+".mp4' "+source_+" -f AVC_720P_1280_2048_192_B")
    sql = "INSERT INTO youtube(id,name) VALUES(%s, %s)"
    cursor.execute(sql, (i, source))
    db.commit()

if int(naver)==0:
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    source = soup.select('#container > h1 > yt-formatted-string')[0].get_text()
    if int(ischeck) == 1:
        sql = 'select max(id) from youtube;'
        cursor.execute(sql)
        rows = cursor.fetchall()
        i = rows[0]
        i = int(i[0])+1
        print(i)
        try:
            os.system('youtube-dl -o '+"/home/choigod1023/izone/public/videos/hd/" +"'(CAM)"+str(i)+".mp4' "+source_+" -f 137")
        except:
            os.system('youtube-dl -o '+"/home/choigod1023/izone/public/videos/hd/" +"'(CAM)"+str(i)+"' "+source_+" -f 22")
        sql = "INSERT INTO youtube(id,name) VALUES(%s, %s)"
        cursor.execute(sql, (i, source))
        db.commit()
    elif int(ischeck) == 0:
        source = input('영상 제목을 영문으로 입력해주십시오: ')
        os.system('youtube-dl -o '+"/home/choigod1023/izone/public/videos/hd/" +
                "'(OTHER) "+source+'.mp4'+"' "+source_+" -f AVC_1080P_1920_5120_192")
db.close()
driver.quit()

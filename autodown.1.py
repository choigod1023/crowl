
from bs4 import BeautifulSoup
import requests
import re
import json
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import pymysql
dd = open("/home/choigod1023/vlivecrowling/temp.txt", "r")
j = int(dd.readline())


def get_videoName(video, video_subject):
    return '/home/choigod1023/vue express/backend/public/videos/hd/[VLIVE] [' + video.get('encodingOption').get('name') + "] " + str(j) + ".mp4"


def get__videoName(video, video_subject, title):
    return '[VLIVE] [' + title + "] " + video_subject + ".mp4"


dd.close()
db = pymysql.connect(host='127.0.0.1', port=3306, user='choigod1023',
                     passwd='jjang486', db='choigod1023', charset='utf8')
cursor = db.cursor()
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(
    '/home/choigod1023/vlivecrowling/chromedriver', chrome_options=options)

for i in range(7,137):

    driver.get('https://channels.vlive.tv/C1B7AF/video')
    time.sleep(5)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(1)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(1)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(1)
    html = driver.execute_script('return document.body.innerHTML')
    thumb = driver.find_element_by_css_selector('#container > channel > div > video-list > div > div > ul > li:nth-child('+str(i)+') > video-list-item > div > a > div.article_img > img').get_attribute('src')
    print(thumb)
    driver.find_element_by_xpath(
        '//*[@id="container"]/channel/div/video-list/div/div/ul/li['+str(i)+']/video-list-item/div/a').click()

    currenturl = driver.current_url
    html = requests.get(currenturl).text
    soup = BeautifulSoup(html, 'html.parser')
    script_tag = soup.find_all('script')[5].text
    regex = "vlive.video.init(.+\s+.+\s+.+)"
    element_list = re.findall(regex, script_tag)[0].split(',')
    video_elements = []

    for element in element_list:
        if len(element) >= 15:
            video_elements.append(element.replace(
                "\t", "").replace("\n", "").replace('"', ""))

    video_html = requests.get(
        'https://apis.naver.com/rmcnmv/rmcnmv/vod/play/v2.0/%s?key=%s' % (video_elements[0], video_elements[1]))
    video_data = json.loads(video_html.text)
    video_list = video_data.get('videos').get('list')
    video_subject = video_data.get('meta').get('subject')

    string = get__videoName(video_list[0], video_subject, '360P').replace(
        '[', '(').replace(']', ')').replace('*', '')
    sql = "SELECT COUNT(*) FROM vlive where NAME=%s"
    cursor.execute(sql, string)
    row3 = cursor.fetchone()
    print(row3[0])

    string = get__videoName(video_list[0], video_subject, '1080P').replace(
        '[', '(').replace(']', ')').replace('*', '')
    cursor.execute(sql, string)
    rows = cursor.fetchone()

    if(int(rows[0]) == 0):
        string = get__videoName(video_list[0], video_subject, '720P').replace(
            '[', '(').replace(']', ')').replace('*', '')
        sql = "SELECT COUNT(*) FROM vlive where NAME=%s"
        cursor.execute(sql, string)
        rows = cursor.fetchone()
    print(rows[0])
    try:
        if not int(rows[0]) and not int(row3[0]):
            print('writing')
            check = 0
            for video in video_list:
                if video.get('encodingOption').get('name') == '1080P':
                    string = get__videoName(video_list[0], video_subject, video.get('encodingOption').get('name')).replace(
                        '[', '(').replace(']', ')').replace('*', '')
                    check = 3
                    break
                elif video.get('encodingOption').get('name')=='720P' and check!=3:
                    string = get__videoName(video_list[0], video_subject, video.get('encodingOption').get('name')).replace(
                        '[', '(').replace(']', ')').replace('*', '')
                    check=2
                elif video.get('encodingOption').get('name')=='360P' and check==0:
                    string = get__videoName(video_list[0], video_subject, video.get('encodingOption').get('name')).replace(
                        '[', '(').replace(']', ')').replace('*', '')
                    check=1
            print(string)
            for video in video_list:
                if video.get('encodingOption').get('name') == '360P' or video.get('encodingOption').get('name') == '720P' or video.get('encodingOption').get('name') == '1080P':
                    print('entering')
                    with urlopen(video.get('source')) as res:
                        res_data = res.read()
                        print('reading')

                        with open(get_videoName(video, video_subject).replace('[', '(').replace(']', ')').replace('*', ''), 'wb') as f:
                            f.write(res_data)

            sql = "INSERT INTO vlive(id, name,thumb) VALUES(%s,%s, %s)"
            cursor.execute(sql, (j, string,thumb))
            dd = open("/home/choigod1023/vlivecrowling/temp.txt", "w")
            j = j-1
            print(j)
            dd.write(str(j))
            db.commit()
        else:
            driver.quit()
    except:
        driver.quit()
print('exit')
driver.quit()
db.close()

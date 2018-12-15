from bs4 import BeautifulSoup
import requests
import re
import json
from urllib.request import urlopen
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pymysql
j=84
def get_videoName(video, video_subject):
    return '../izone/public/videos/hd/[VLIVE] [' + video.get('encodingOption').get('name') + "] " + str(j) + ".mp4"
def get__videoName(video, video_subject):
    return '[VLIVE] [' + video.get('encodingOption').get('name') + "] " + video_subject + ".mp4"

dd= open("temp.txt","r")
# db = pymysql.connect(host='127.0.0.1', port=3306, user='choigod1023', passwd='jjang486', db='choigod1023', charset='utf8')
# cursor = db.cursor()
txtdate = dd.read()
# options = Options()
# options.add_argument("--headless")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
txtdate = datetime.datetime.strptime(txtdate,"%Y-%m-%d %H:%M:%S")
driver = webdriver.Chrome('./chromedriver.exe')
#, chrome_options=options)

driver.get('https://channels.vlive.tv/C1B7AF/video')
time.sleep(3)
html = driver.execute_script('return document.body.innerHTML')
soup = BeautifulSoup(html, 'html.parser')
table = driver.find_element_by_xpath('//*[@id="container"]/channel/div/video-list/div/div/ul/li[1]/video-list-item/div/a/div[2]/div/strong')
table_data = table.text
print(table_data)
if '분 전' in table_data:
    m = int(table_data.replace("분 전",""))
    date = datetime.datetime.now()
    minutes_later = date-datetime.timedelta(minutes=m)
    print(minutes_later)
    result = txtdate-minutes_later
    if int(result.days)<0:
        driver.find_element_by_xpath('//*[@id="container"]/channel/div/video-list/div/div/ul/li[1]/video-list-item/div/a').click()
        currenturl = driver.current_url
        html = requests.get(currenturl).text
        soup = BeautifulSoup(html, 'html.parser')
        script_tag = soup.find_all('script')[5].text
        regex = "vlive.video.init(.+\s+.+\s+.+)"
        element_list = re.findall(regex, script_tag)[0].split(',')
        video_elements = []

        for element in element_list:
            if len(element) >= 15:
                video_elements.append(element.replace("\t", "").replace("\n", "").replace('"', ""))

        video_html = requests.get('https://apis.naver.com/rmcnmv/rmcnmv/vod/play/v2.0/%s?key=%s' % (video_elements[0], video_elements[1]))
        video_data = json.loads(video_html.text)
        video_list = video_data.get('videos').get('list')
        video_subject = video_data.get('meta').get('subject')

        for video in video_list:
            if video.get('encodingOption').get('name') == '480P' or video.get('encodingOption').get('name') == '720P':
                with urlopen(video.get('source')) as res:
                    res_data = res.read()
                    with open(get_videoName(video, video_subject).replace('[', '(').replace(']', ')').replace('*', ''), 'wb') as f:
                        f.write(res_data)
if '시간 전' in table_data:
    m = int(table_data.replace("시간 전",""))+1
    print(m)
    date = datetime.datetime.now()
    minutes_later = date-datetime.timedelta(hours=m)
    print(minutes_later)
    result = minutes_later-txtdate
    print(result)
    if int(result.days)<0:
        driver.find_element_by_xpath('//*[@id="container"]/channel/div/video-list/div/div/ul/li[1]/video-list-item/div/a').click()
        currenturl = driver.current_url
        html = requests.get(currenturl).text
        soup = BeautifulSoup(html, 'html.parser')
        script_tag = soup.find_all('script')[5].text
        regex = "vlive.video.init(.+\s+.+\s+.+)"
        element_list = re.findall(regex, script_tag)[0].split(',')
        video_elements = []

        for element in element_list:
            if len(element) >= 15:
                video_elements.append(element.replace("\t", "").replace("\n", "").replace('"', ""))

        video_html = requests.get('https://apis.naver.com/rmcnmv/rmcnmv/vod/play/v2.0/%s?key=%s' % (video_elements[0], video_elements[1]))
        video_data = json.loads(video_html.text)
        video_list = video_data.get('videos').get('list')
        video_subject = video_data.get('meta').get('subject')

        for video in video_list:
            if video.get('encodingOption').get('name') == '480P' or video.get('encodingOption').get('name') == '720P':
                with urlopen(video.get('source')) as res:
                    res_data = res.read()
                    with open(get_videoName(video, video_subject).replace('[', '(').replace(']', ')').replace('*', ''), 'wb') as f:
                        f.write(res_data)
else:
    exit()
string = get__videoName(video, video_subject).replace('[', '(').replace(']', ')').replace('*', '')
sql = "INSERT INTO vlive(id, name) VALUES(%s, %s)"
# cursor.execute(sql, (j, string)) 
ww = open("temp.txt","w")
ww.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
exit()
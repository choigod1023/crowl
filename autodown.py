from bs4 import BeautifulSoup
import requests
import re
import json
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
j=98
def get_videoName(video, video_subject):
    return './[VLIVE] [' + video.get('encodingOption').get('name') + "] " + str(j) + ".mp4"
def get__videoName(video, video_subject):
    return '[VLIVE] [' + video.get('encodingOption').get('name') + "] " + video_subject + ".mp4"

driver = webdriver.Chrome('./chromedriver.exe')

for i in range(1,3):
    
    driver.get('https://channels.vlive.tv/C1B7AF/video')
    time.sleep(3)
    html = driver.execute_script('return document.body.innerHTML')
    driver.find_element_by_xpath('//*[@id="container"]/channel/div/video-list/div/div/ul/li['+str(i)+']/video-list-item/div/a').click()

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
    string = get__videoName(video, video_subject).replace('[', '(').replace(']', ')').replace('*', '')
    ddd = {}
    ddd.update({i:string})
    j=j-1
with open('data.json', 'w', encoding="utf-8") as make_file:
    json.dump(dict, make_file, ensure_ascii=False, indent="\t")
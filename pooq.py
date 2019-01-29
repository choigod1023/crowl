from selenium import webdriver
import time
import os
driver = webdriver.Chrome('./chromedriver.exe')

driver.get('https://www.pooq.co.kr/member/login.html?referer=https%3A%2F%2Fwww.pooq.co.kr%2Findex.html')


a = input("아이디")
b = input("비밀번호")
time.sleep(5)
driver.find_element_by_css_selector('body > div.body > div.member > div > form > ul.input-wrap01 > li:nth-child(1) > input').send_keys(a)
driver.find_element_by_css_selector('body > div.body > div.member > div > form > ul.input-wrap01 > li:nth-child(2) > input').send_keys(b)
driver.find_element_by_css_selector('body > div.body > div.member > div > form > div > a').click()
time.sleep(3)
driver.find_element_by_css_selector('body > div > div > div.tAc > div > div:nth-child(1) > a:nth-child(1)').click()
time.sleep(3)
driver.get('https://www.pooq.co.kr/player/vod.html?programid=C9901_C99000000002&contentid=C9901_C99000000002_01_0005.1')
time.sleep(3)
driver.get('https://vod-c9901.cdn.pooq.co.kr/hls/C9901/C9901_C99000000002_01_0005.1/1/1000/chunklist.m3u8')
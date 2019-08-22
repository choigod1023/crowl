import random
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome('chromedriver.exe')
import os
import requests
from urllib.parse import urlencode, quote_plus
targeturl="https://www.google.com/recaptcha/api2/demo"
apikey="4c7a580a6fe68ba1fa801dad9ba0550d"

driver.get(targeturl)
gk=driver.find_element_by_id("recaptcha-demo").get_attribute("data-sitekey")
fmturl="http://2captcha.com/in.php?key={0}&method=userrecaptcha&googlekey={1}&pageurl={2}"
url=fmturl.format(apikey,gk,quote_plus(targeturl))
res=requests.get(url)
sk=res.text.split("|")

if sk[0]=="OK":
    reqcomp=False
    tkn=None
    while not reqcomp:
        fmturl="http://2captcha.com/res.php?key={0}&action=get&id={1}"
        url=fmturl.format(apikey,sk[1])
        res=requests.get(url)
        if res.text!="CAPCHA_NOT_READY":
            reqcomp=True
            tkn=res.text
        else:
            print("waiting...")
            time.sleep(5)
    print(tkn)
    driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML="{0}";'.format(tkn.split("|")[1]))

else:
    print("failed")

input()
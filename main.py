from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from urllib.request import urlopen
import json

import re


def open_site(url):
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    driver = webdriver.Chrome(desired_capabilities=caps)
    driver.get(url)
    time.sleep(10)  # wait for all the data to arrive.
    perf = driver.get_log('performance')
    start = 'timed'
    end = 'vt=3'
    listToStr = ' '.join(map(str, perf))
    sub = listToStr[listToStr.find(start):listToStr.find(end) + len(end)]
    return "https://www.youtube.com/api/" + sub


def proces_json():
    url ='https://www.youtube.com/api/timedtext?v=Y2NkuFIlLEo&exp=xftt%2Cxctw&xoaf=5&hl=pl&ip=0.0.0.0&ipbits=0&expire=1640408762&sparams=ip%2Cipbits%2Cexpire%2Cv%2Cexp%2Cxoaf&signature=1D2C5904EFB9B478B375DE5F334146CA6CC9F0D4.B18D84EFF390C45B3776918DBEE0BD02D86B40DA&key=yt8&lang=en&name=en&fmt=json3&xorb=2&xobt=3&xovt=3'
    # store the response of URL
    response = urlopen(url)
    data_json = json.loads(response.read())

    for x in range(1, len(data_json['events'])):

        cc = (data_json['events'][x]['segs'][0])
        start_ms = (data_json['events'][x]['tStartMs'])
        duration_ms = (data_json['events'][x]['dDurationMs'])

        temp = time.strftime('%H:%M:%S.{}'.format(start_ms%1000), time.gmtime(start_ms/1000.0))
        temp1 = time.strftime('%H:%M:%S.{}'.format((duration_ms+start_ms)%1000), time.gmtime((duration_ms+start_ms)/1000.0))

        print(x)
        print(temp, '-->', temp1)
        print(cc.get('utf8'))
        print('\n')


if __name__ == "__main__":
    start = time.time()
    # url = 'https://www.youtube.com/watch?v=Y2NkuFIlLEo'
    # open_site(url)
    proces_json()

    print("Znalezienie linku zajelo:", time.time() - start, "seconds.")

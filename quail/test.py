import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time 

import os


### url 가져오기

## 카카오 맵 
driver = webdriver.Chrome()
driver.get('https://map.kakao.com/')
time.sleep(2)

## input 창에 검색어 입력
searchbox = driver.find_element(By.ID, 'search.keyword.query')
searchbox.send_keys('홍대 맛집'+ Keys.ENTER)
time.sleep(3)

## 상세보기 주소 가져오기 
list_url = []

for inx in range(2,4):     # (시작값, 종료값):   # 일단 1page 까지만
    moreview_element = driver.find_elements(By.CSS_SELECTOR, 'a[data-id="moreview"]')
    for i in range(len(moreview_element)):
        list_url.append(moreview_element[i].get_attribute('href'))
    if inx == 2:
        driver.find_element(By.ID, 'info.search.place.more').click()
        time.sleep(1)
    else:
        driver.find_element(By.ID, f'info.search.page.no{inx}').click()
        time.sleep(1)


## 웹페이지 종료
driver.close()


### 정보 넣을 빈 딕셔너리
data = {
    'name' : [],
    'category' : [],
    'star' : [],
    'address' : [],
    'oper_time' : [],
    'starCount' : [],
    'reviewCount' : []
}



### 기본 정보 크롤링 (상세보기 get으로 열어서 가져오기)

for i in range(len(list_url)):
    ## 상세보기 웹페이지 열기
    driver = webdriver.Chrome()
    driver.get(list_url[i])
    driver.implicitly_wait(3)

    # 영업시간 더 보기 클릭
    try:
        oper_more = driver.find_elements(By.CSS_SELECTOR, 'a[data-logevent = "main_info,more_timeinfo"]')
        oper_more[0].clcik()
        time.sleep(2)

         ## 상세page bs4 파싱 분석
        soup = bs(driver.page_source, 'html.parser')

    # 영업시간 더보기가 없는 경우
    except:
        ## 상세page bs4 파싱 분석
        soup = bs(driver.page_source, 'html.parser')

    # 웹페이지 닫기
    driver.close()
    
    ## 매장명
    data['name'].append(soup.find('h2', {'class':'tit_location'}).get_text())
    ## 분류
    data['category'].append(soup.find('span',{'class':'txt_location'}).get_text().split(':')[1].strip())
    ## 주소
    data['address'].append(soup.find('span', {'class': 'txt_address'}).get_text().replace(" ", "").replace("\n", " "))

    ## 별점, 리뷰 수 
    # 별점 있는 경우
    if len(soup.find_all('span',{'class':'color_b'})) > 1:
        data['star'].append(soup.find_all('span', {'class':'color_b'})[0].get_text().strip('점'))
        data['starCount'].append(soup.find('a', {'class': 'link_evaluation'})['data-cnt'])
        data['reviewCount'].append(soup.find_all('span', {'class':'color_b'})[1].get_text().strip('개'))
    # 별점 없는 경우
    else:
        data['star'].append('0')
        data['starCount'].append('0')
        data['reviewCount'].append(soup.find('span', {'class':'color_b'}).get_text().strip('개'))

    ## 영업시간
    # 더보기 있는 경우
    if oper_more:    
        data['oper_time'].append(soup.find_all('ul', {'class':'list_operation'})[1].get_text().strip())
    # 더보기 없는 경우
    else:
        data['oper_time'].append(soup.find('ul', {'class':'list_operation'}).get_text().strip().replace("\n", ""))

    print(f"{i+1}번째 데이터 입력 완료")

df = pd.DataFrame(data)
df.to_csv("data.csv", index=False)
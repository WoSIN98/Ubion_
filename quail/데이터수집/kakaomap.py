import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time 
import base64

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

## 아래 1,2,3,4,5 리스트 번호 다 뜨도록
# 장소 더보기 클릭
driver.find_element(By.ID, 'info.search.place.more').click()
time.sleep(2)
# 1번리스트로 돌아오기
driver.find_element(By.ID, 'info.search.page.no1').click()
time.sleep(2)

for count in range(1):
    
    for inx in range(2, 6):
        
        # 현재 리스트의 상세보기 주소 스크래핑
        moreview_element = driver.find_elements(By.CSS_SELECTOR, 'a[data-id="moreview"]')
        for i in range(len(moreview_element)):
            list_url.append(moreview_element[i].get_attribute('href'))
        # 다음 리스트 클릭
        driver.find_element(By.ID, f'info.search.page.no{inx}').click()
        # 5번 리스트 저장
        if inx == 5:
            moreview_element = driver.find_elements(By.CSS_SELECTOR, 'a[data-id="moreview"]')
            for i in range(len(moreview_element)):
                list_url.append(moreview_element[i].get_attribute('href'))
        time.sleep(2)
    # 다음 리스트 페이지 넘어가기
    driver.find_element(By.ID ,'info.search.page.next').click()
    time.sleep(2)



## 웹페이지 종료
driver.close()


## 정보 넣을 빈 딕셔너리
data = {
    'merchant' : [],
    'category' : [],
    'star' : [],
    'address' : [],
    'oper_time' : [],
    'starCount' : [],
    'reviewCount' : []
}

### 기본 정보 크롤링 (상세보기 get으로 열어서 가져오기)
driver = webdriver.Chrome()
for i in range(len(list_url)):

    data2 = {
    'user_name' : [],
    'user_rank' : [],
    'num_response' : [],
    'user_star' : [], 
    'time' : [],
    'rating' : [],
    'content' : []
    }

    ## 상세보기 웹페이지 열기
    driver.get(list_url[i])
    driver.implicitly_wait(3)

    # 영업시간 더 보기 클릭
    try:
        oper_more = driver.find_elements(By.CSS_SELECTOR, 'a[data-logevent = "main_info,more_timeinfo"]')
        oper_more[0].click()
        time.sleep(2)  

    # 영업시간 더보기가 없는 경우
    except:
        pass

    # 후기 더보기 클릭
    try:
        link_more = driver.find_element(By.CLASS_NAME, 'txt_more')
        while link_more.text == "후기 더보기":
            link_more = driver.find_element(By.CLASS_NAME, 'txt_more')
            # 마지막 후기 더보기까지 눌렀으면 멈추기
            if link_more.text != "후기 접기":
                link_more.click()
                time.sleep(0.3)
    # 후기 더보기 없는 경우        
    except:
        pass
    time.sleep(0.1)
  
    ## 상세page bs4 파싱 분석
    soup = bs(driver.page_source, 'html.parser')

    try:
        ##canvas 이미지 저장

        test_image = driver.execute_script("return document.querySelectorAll('canvas')[1].toDataURL();")
        image_data = test_image.split(',')[1]

        ## Base64 디코딩하여 이미지 데이터 추출
        image_data_decoded = base64.b64decode(image_data)

        test_image2 = driver.execute_script("return document.querySelectorAll('canvas')[2].toDataURL();")
        image_data2 = test_image2.split(',')[1]

        ## Base64 디코딩하여 이미지 데이터 추출
        image_data_decoded2 = base64.b64decode(image_data2)
    except:
        pass

        
    


    ## 매장명
    mer = soup.find('h2', {'class':'tit_location'}).get_text()
    data['merchant'].append(mer)
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


    # 리뷰 목록 잡기
    reveiw_listed = soup.find_all('li', {'data-ismy':'false'})

    #### df2 만들기 (리뷰df)
    for j in range(len(reveiw_listed)):
        ## 유저 이름
        data2['user_name'].append(soup.find_all('span',{'class':'txt_username'})[j].get_text())
        ## 유저 레벨
        data2['user_rank'].append(soup.find_all('span', {'class' : 'txt_badge'})[j].get_text().strip('레벨'))
        ## 유저 후기수
        data2['num_response'].append(
            soup.find_all('div',{'class':'unit_info'})[j].find_all('span',{'class':'txt_desc'})[0].get_text()
        )
        ## 유저 별점 평균
        data2['user_star'].append(
            soup.find_all('div',{'class':'unit_info'})[j].find_all('span',{'class':'txt_desc'})[1].get_text()
        )
        ### 리뷰 작성 시간
        data2['time'].append(
            soup.find_all('div',{'class':'unit_info'})[j].find('span',{'class':'time_write'}).get_text()
        )
        ## 리뷰 내용
        data2['content'].append(
            soup.find_all('p', {'class':'txt_comment'})[j].get_text().strip('더보기')
        )

        ## 유저가 평가한 별점 
        # 너비를 추출하여 별점 계산 (너비는 별점의 백분율을 나타냄)
        style_attribute = soup.find_all('div', {'class':'star_info'})[j].find('span',{'class':'ico_star inner_star'})['style']
        width_percent = float(style_attribute.split(':')[1].strip('%;'))
        rating_out_of_five = width_percent / 20  # 별점은 100%를 5로 나눈 값
        data2['rating'].append(rating_out_of_five)

    ## 데이터 프레임으로 만들기
    df2 = pd.DataFrame(data2)
    df2.to_csv(f'./data2/{mer}.csv',index = False)

    try:
        # 이미지 데이터를 파일로 저장
        with open(f'./image/{mer}1.png', 'wb') as f:
            f.write(image_data_decoded)

        with open(f'./image/{mer}2.png', 'wb') as f:
            f.write(image_data_decoded2)
    except:
        pass

    

    print(f"{i+1}번째 데이터 입력 완료, {mer}.csv 저장 완료")

driver.close()

df = pd.DataFrame(data)
df.to_csv("./data1/data.csv", index=False)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os 
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

# 이미지를 저장하는 함수 생성
def image_save(img_path, save_path, file_name):
    html_data = requests.get(img_path)
    imageFile = open(
        os.path.join(
            save_path,
            file_name
        ),
        'wb'
    )
    # 이미지 데이터의 크기
    chunk_size = 100000000
    for chunk in html_data.iter_content(chunk_size):
        imageFile.write(chunk)
        imageFile.close()
    print('파일 저장 완료')

driver = webdriver.Chrome()
time.sleep(1)
driver.get('https://m.naver.com')

time.sleep(3)

element = driver.find_element(By.ID, 'MM_SEARCH_FAKE')
element.click()
time.sleep(1)
element2 = driver.find_element(By.ID, 'query')
element2.send_keys('서울숲 클라이밍'+Keys.ENTER)


time.sleep(3)
driver.find_element(By.CLASS_NAME, 'YXb5L').find_element(By.CSS_SELECTOR, 'a').click()

time.sleep(3)
driver.find_element(By.ID, '_place_portal_root').find_element(By.CSS_SELECTOR,'a').click()

# 3번째 열기

for num in range(2):
    
    time.sleep(3)
    driver.find_elements(By.CLASS_NAME, 'ouxiq')[num].find_element(By.CSS_SELECTOR, 'a').click()

    # 리뷰버튼 누르기
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, 'flicking-camera').find_elements(By.CSS_SELECTOR, 'a')[3].click()

    # 댓글 더보기 버튼 누르기
    time.sleep(2)
    for j in range(4):
        try:
            driver.find_elements(By.CLASS_NAME,'rvCSr')[j].click()
        except:
            continue

    soup = bs(driver.page_source, 'html.parser')

    li_list = soup.find_all('li', attrs={'class' : 'owAeM'})

    reviews = []
    i = 1
    for li_data in li_list:
        review_data = li_data.find('span', {'class':'zPfVt'}).get_text()
        reviews.append(review_data)
        div_data = li_data.find('div', {'class':'VAvOk'})

        try:
            img_list = div_data.find_all('img')

            for img in img_list:
                file_name = f"review_{num}_{i}.png"
                save_path = './img/'
                image_save(img['src'], save_path, file_name)
                i += 1
        except:
            continue

    data = pd.Series(reviews)
    data.to_excel(f'reviews{num}.xlsx')

    driver.back()
    driver.back()

    time.sleep(1)
    driver.find_element(By.ID, '_place_portal_root').find_element(By.CSS_SELECTOR,'a').click()

driver.close()
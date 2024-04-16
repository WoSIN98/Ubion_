from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import time
from dotenv import load_dotenv
import requests
from konlpy.tag import Okt

load_dotenv()

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

def search_insta(_text):
    # _text : 인스타그램 검색어를 인자값으로 저장하는 변수
    driver = webdriver.Chrome()
    driver.get('https://www.instagram.com')

    driver.implicitly_wait(5)

    face_element = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[5]/button')
    face_element.click()
    driver.implicitly_wait(5)

    id_element = driver.find_element(By.XPATH, '//*[@id="email"]')
    id_element.send_keys(os.getenv('id'))
    pass_element = driver.find_element(By.XPATH, '//*[@id="pass"]')
    pass_element.send_keys(os.getenv('password'))
    pass_element.send_keys(Keys.ENTER)
    
    driver.implicitly_wait(15)
    search_element = driver.find_element(By.CSS_SELECTOR, 'svg[aria-label="검색"]')
    # search_elemnet를 클릭
    search_element.click()

    driver.implicitly_wait(10)
    # 검색창에 input태그를 선택
    search_input = driver.find_element(By.CSS_SELECTOR,'input[aria-label="입력 검색"]')

    # search_input에 특정 문자열을 입력
    search_input.send_keys(_text)

    # class명들 노타빌리티 메모 확인
    driver.implicitly_wait(10)
    ## 검색 리스트 전체를 검색
    list_element = driver.find_elements(
        By.CSS_SELECTOR, '.x9f619.x78zum5.xdt5ytf.x1iyjqo2.x6ikm8r.x1odjw0f.xh8yej3.xocp1fn .x1i10hfl.x1qjc9v5.xjbqb8w.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1q0g3np.x87ps6o.x1lku1pv.x1a2a7pz.x1dm5mii.x16mil14.xiojian.x1yutycm.x1lliihq.x193iq5w.xh8yej3')
    list_element[1].click()

    driver.implicitly_wait(10)

    time.sleep(1)
    ## 게시글 링크를 모두 찾는다.
    imgs = driver.find_elements(By.CSS_SELECTOR, '._aagw')

    imgs[0].click()

    # data를 저장할 공간 생성
    data = {
        'ID': [],
        'Comment' : []
    }
    driver.implicitly_wait(20)
    for i in range(3):
        
        try:
            driver.implicitly_wait(10)
            ids = driver.find_elements(By.CSS_SELECTOR, 'h2[class="_a9zc"]')

            ids.extend(driver.find_elements(By.CSS_SELECTOR,'h3[class="_a9zc"]'))
            
            comments = driver.find_elements(By.CSS_SELECTOR, 'div[class="_a9zs"]')
            
            img_element = driver.find_element(By.CSS_SELECTOR, '._aagu._aato ._aagv .x5yr21d.xu96u03.x10l6tqk.x13vifvy.x87ps6o.xh8yej3')
        
            img_src = img_element.get_attribute('src')

            # print(img_src)
            

            image_save(img_src, "./", f"{_text}_{i}.png")

            for id, comment in zip(ids, comments):
                data['ID'].append(id.text)
                data['Comment'].append(comment.text.replace("\n", ""))
            next_element = driver.find_element(By.CSS_SELECTOR, '._aaqg ._abl-')
            next_element.click()
        except:
            print('다음 버튼이 존재하지 않거나 에러 발생')
            
            next_element = driver.find_element(By.CSS_SELECTOR, '._aaqg ._abl-')
            next_element.click()

    # 게시물을 닫아주기.
    close_element = driver.find_element(By.CSS_SELECTOR, 'svg[aria-label="닫기"]')
    close_element.click()
    df = pd.DataFrame(data)

    okt = Okt()

    col_data = []
    for i in range(len(df)):
        nouns = okt.nouns(df.loc[i,'Comment'])

        if nouns:
            words = [n for n in nouns if len(n) > 1]
        else:
            words = ''
        col_data.append(words)
    df['words'] = col_data    
    
    
    df.to_csv(f'{_text}.csv', index=False)

    ## 웹 브라우저 종료
    driver.close()
    
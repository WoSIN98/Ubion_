import os
from glob import glob
import pandas as pd

## 파일을 데이터프레임으로 로드하는 함수 하나 생성 
# 매개변수 2개 : 상대경로 | 절대경로 , encording = 'utf-8'
def read_df(_path, _encoding = 'utf-8'):
    # 입력받은 데이터에서 확장자를 분리해준다. 
    head, tail = os.path.splitext(_path)
    # print(tail)
    if tail == '.csv':
        df = pd.read_csv(_path, encoding = _encoding)
    elif tail == '.json':
        df = pd.read_json(_path, encoding = _encoding)
    elif tail == '.xml':
        df = pd.read_xml(_path, encoding = _encoding)
    elif tail in ['.xlsx', '.xls']:
        df = pd.read_excel(_path)                              
    else:
        df = pd.DataFrame()
    return df


#### 지정된 경로에 파일들을 하나의 데이터프레임으로 결합하여 되돌려주는 함수 생성
# 매개변수 -> 경로, 확장자명 
def data_load(_path, _end = 'csv'):
    # _path : 파일의 경로
    # _end : 파일의 확장자명

    # 유저가 입력한 경로를 이용하여 파일의 리스트를 변수에 저장 
    file_list = os.listdir(_path)
    # 비어있는 데이터프레임 생성
    result = pd.DataFrame()
    _path = _path + '/'
    # _path에 '\'의 값을 '/' 대체
    # _path = _path.replace('\','/')
    for file in file_list:
        # file -> 파일명 
        # 파일명의 확장자가 유저가 입력한 확장자와 같다면 
        if file.endswith(_end):
            try: 
                df = read_df(_path+file)                                                   # 이걸 시도
            except:                                                                        # 실패하면 아래를 시도
                try:
                    df = read_df(_path+file, 'CP949')
                except:                                                                       
                    df = read_df(_path+file, 'EUC-KR')               
            #df를 result에 유니언 결합
            result = pd.concat([result, df], axis = 0, ignore_index = True)
    return result        

## 특정 경로에 있는 파일의 목록들을 각각 파일의 이름으로 변수 생성하는 함수   
# 매개변수 : 경로
def data_load2(_path):
    # 입력받은 경로를 기준으로 파일의 목록을 모두 로드한다.
    file_list = glob(_path+'/*.*')

    # 비어있는 딕셔너리 데이터를 생성
    result = dict()                                # result = {}
    # 반복 실행 file_list를 이용하여 
    for file in file_list:
        # 경로와 파일명을 나눠준다.
        folder, name = os.path.split(file)
        # 파일명에서 이름과 확장자를 나눠준다.
        head, tail = os.path.splitext(name)
        # tail의 형태는 : ".확장자"
        try:
            df = read_df(file)                                                  
        except:                                                                      
            try:
                df = read_df(file, 'CP949')
            except:                                                                       
                df = read_df(file, 'EUC-KR')  
        if len(df) != 0:
            result[f'{head}'] = df.copy()
            print(f"{head} 변수 저장 완료")
        else:
            print("지원하지 않는 확장자 파일")                                 # 여기서는 continue 왜 안쓰는 지 확인 녹음 4:11, 밑에 코드가 없으므로 쓰나 안쓰나 똑같다.
    return result
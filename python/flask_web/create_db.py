## 데이터베이스에 테이블을 생성하는 쿼리문들을 모아서 저장
import database 

## 서버 정보를 입력 (Class 생성)
_db = database.MyDB()

## 게시판 테이블을 생성하는 쿼리문을 작성 
board_create = """
    CREATE TABLE 
    IF NOT EXISTS  
    `board`(
        No int primary key auto_increment,
        title text not null,
        writer varchar(32) not null,
        create_dt varchar(64) not null,
        content text 
    )
"""
    # IF NOT EXSITS : 존재하지 않을 때만 쿼리문을 실행하겠다.
result = _db.sql_query(board_create)
print(result)

# > python create_db.py
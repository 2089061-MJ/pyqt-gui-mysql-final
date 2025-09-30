# 의류 재고 관리 프로그램
import pymysql

DB_CONFIG = dict(
    host = "localhost",
    user = "root",
    password = "test0123",
    database = "clothes",
    charset = "utf8"
)

class DB:
    def __init__(self, **config):   # **config : 딕셔너리 전개
        self.config = config
        
    def connect(self):
        return pymysql.connect(**self.config)
    
    def verify_user(self, username, password):
        sql = "SELECT COUNT(*) FROM users WHERE username=%s AND password=%s"
        with self.connect() as conn:
            with conn.cursor()as cur:
                cur.execute(sql, (username, password))
                # SELECT는 행 단위로 가져와! fetchone의 결과는 튜플!
                count, = cur.fetchone()
                return count == 1
            
    def fetch_clothes(self):
        sql = "SELECT * FROM management ORDER BY id"
        with self.connect() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return cur.fetchall()
            
    def insert_clothes(self, name, price, stock):
        sql = "INSERT INTO management (name, price, stock) VALUES (%s, %s, %s)"
        with self.connect() as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (name, price, stock))
                conn.commit()
                return True
            except Exception:
                conn.rollback()
                return False
            
    def delete_item(self, mid):
        sql = "DELETE FROM management WHERE ID=%s"
        with self.connect()as conn:
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, (mid,))
                conn.commit()
                return True
            except Exception:
                print("삭제중 오류 발생")
                conn.rollback()
                return False
from mysql.connector import pooling
import os
from dotenv import load_dotenv

# 使用.env隱藏私密訊息
load_dotenv()
sql_user = os.getenv("sql_user")
sql_password = os.getenv("sql_password")

connection_pool = pooling.MySQLConnectionPool(
    pool_name="py_pool",
    pool_size=32,
    pool_reset_session=True,
    host="localhost",          # 主機名稱
    database="taipei_day_trip",  # 資料庫名稱
    user=sql_user,        # 帳號
    password=sql_password)  # 密碼
from flask import *
from mysql.connector import pooling
import os
from dotenv import load_dotenv
from mysql_connect import connection_pool
# 使用.env隱藏私密訊息
load_dotenv()
sql_user = os.getenv("sql_user")
sql_password = os.getenv("sql_password")

# 初始化blueprint
category = Blueprint("category", __name__)

# 設定Session的密鑰
secret_key = os.getenv("secret_key")
category.secret_key = secret_key


@ category.route("/api/categories", methods=["GET"])  # 取得景點分類名稱列表
def find_categories():
    try:
        result = {"data": None}
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor(dictionary=True)
        query = "SELECT category FROM attraction GROUP BY category;"
        cursor.execute(query)
        record = cursor.fetchall()
        result["data"] = record
        data_str = []
        for i in record:
            data = i["category"]
            data_str.append(data)
        result["data"] = data_str
        return jsonify(result), 200
    except:
        return jsonify({"error": True, "message": "找不到任何訊息，伺服器錯誤"}), 500
    finally:
        cursor.close()
        connection_object.close()

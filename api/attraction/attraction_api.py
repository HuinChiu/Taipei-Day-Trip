from flask import *
from mysql.connector import pooling
import ssl
import os
from dotenv import load_dotenv
from mysql_connect import connection_pool
# 使用.env隱藏私密訊息
load_dotenv()
sql_user = os.getenv("sql_user")
sql_password = os.getenv("sql_password")

# 安全憑證
ssl._create_default_https_context = ssl._create_unverified_context

# 初始化blueprint
attraction = Blueprint("attraction", __name__)


@attraction.route("/api/attractions", methods=["GET"])  # 取得景點列表
def getattractions():
    page = int(request.args.get("page", 0))  # 取得頁碼
    start_num = page * 12  # 取得頁碼中的12比資料
    result = {"nextPage": page+1, "data": []}
    keyword = request.args.get("keyword", "None")
    keywordstring = "%"+keyword+"%"
    # 連接資料庫
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor(dictionary=True)
    # 判斷keyword，keyword=None，代表顯示所有資料
    if keyword == "None":
        # 找出所有項目總和
        query1 = "SELECT count(*) FROM attraction;"
        cursor.execute(query1)
        record1 = cursor.fetchone()
        all_count = record1["count(*)"]
        # 從第幾比開始查找12比並顯示
        query = "select * from attraction ORDER BY id LIMIT %s, 12;"
        cursor.execute(query, (start_num,))
        record = cursor.fetchall()  # 每次查詢出來只會有12筆
        result["data"] = record
        count = (len(record))
        cursor.close()
        connection_object.close()
        if count == 0:
            return jsonify({"erro": True, "message": "找不到任何訊息，請重新輸入關鍵字或頁數"}), 500
        else:
            # 假如頁數4(start_num=48)+12=60大於all_count=58，nextPage=null
            if start_num+12 > all_count:
                result["nextPage"] = None
            for i in range(count):
                images = record[i]["images"].split(",")
                record[i]["images"] = images  # 將image分開變成列表回傳
            return jsonify(result), 200
    else:
        # 完全比對＆模糊比對
        query = "select * from attraction where category LIKE %s OR name LIKE %s ORDER BY id LIMIT %s, 12;"
        cursor.execute(query, (keywordstring, keywordstring, start_num))
        record = cursor.fetchall()
        result["data"] = record
        cursor.close()
        connection_object.close()
        count = (len(record))
        if count == 0:
            return jsonify({"erro": True, "message": "找不到任何訊息，請重新輸入關鍵字或頁數"}), 500
        else:
            if start_num+12 > count:
                result["nextPage"] = None
            for i in range(count):
                images = record[i]["images"].split(",")
                record[i]["images"] = images  # 將image分開變成列表回傳
            return jsonify(result), 200


# 根據景點編號取得景點資料
@ attraction.route("/api/attraction/<attractionId>", methods=["GET"])
def attraction_id(attractionId):
    try:
        result = {"data": None}
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor(dictionary=True)
        query = "SELECT * FROM attraction WHERE id=%s;"  # 完全比對＆模糊比對
        cursor.execute(query, (attractionId,))
        record = cursor.fetchone()
        result["data"] = record
        print("attractionID get close")
        if record == None:
            return jsonify({"erro": True, "message": "找不到任何訊息，景點編號輸入錯誤，請重新輸入景點編號"}), 400
        else:
            images = record["images"].split(",")
            record["images"] = images
            return jsonify(result), 200
    except:
        return jsonify({"erro": True, "message": "伺服器錯誤，請稍後再試"}), 500
    finally:
        cursor.close()
        connection_object.close()
        print("attractionIDget close")

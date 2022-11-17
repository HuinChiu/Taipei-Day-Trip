from flask import *
from mysql.connector import pooling
import ssl
import os
from dotenv import load_dotenv

# 初始化flask
app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/")
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['JSON_SORT_KEYS'] = False

# 使用.env隱藏私密訊息
load_dotenv()
sql_user = os.getenv("sql_user")
sql_password = os.getenv("sql_password")

# 安全憑證
ssl._create_default_https_context = ssl._create_unverified_context

# 登入資mysql料庫
connection_pool = pooling.MySQLConnectionPool(
    pool_name="py_pool",
    pool_size=5,
    pool_reset_session=True,
    host="localhost",          # 主機名稱
    database="taipei_day_trip",  # 資料庫名稱
    user=sql_user,        # 帳號
    password=sql_password)  # 密碼

# 設定Session的密鑰
secret_key = os.getenv("secret_key")
app.secret_key = secret_key

# Pages


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/attraction/<id>")
def attraction(id):
    return render_template("attraction.html")


@app.route("/booking")
def booking():
    return render_template("booking.html")


@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")


@app.route("/api/attractions", methods=["GET"])  # 取得景點列表
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
        connection_object.close()
        cursor.close()
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
        print(count)
        if count == 0:
            return jsonify({"erro": True, "message": "找不到任何訊息，請重新輸入關鍵字或頁數"}), 500
        else:
            if start_num+12 > count:
                result["nextPage"] = None
            for i in range(count):
                images = record[i]["images"].split(",")
                record[i]["images"] = images  # 將image分開變成列表回傳
                return jsonify(result), 200


@ app.route("/api/attraction/<attractionId>", methods=["GET"])  # 根據景點編號取得景點資料
def attraction_id(attractionId):
    try:
        result = {"data": None}
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor(dictionary=True)
        query = "SELECT * FROM attraction WHERE id=%s;"  # 完全比對＆模糊比對
        cursor.execute(query, (attractionId,))
        record = cursor.fetchone()
        result["data"] = record
        print(record)
        cursor.close()
        connection_object.close()
        if record == None:
            return jsonify({"erro": True, "message": "找不到任何訊息，景點編號輸入錯誤，請重新輸入景點編號"}), 400
        else:
            images = record["images"].split(",")
            record["images"] = images
            return jsonify(result), 200
    except:
        return jsonify({"erro": True, "message": "伺服器錯誤，請稍後再試"}), 500


@ app.route("/api/categories", methods=["GET"])  # 取得景點分類名稱列表
def find_categories():
    try:
        result = {"data": None}
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor(dictionary=True)
        query = "SELECT category FROM attraction GROUP BY category;"
        cursor.execute(query)
        record = cursor.fetchall()
        result["data"] = record
        cursor.close()
        connection_object.close()
        data_str = []
        for i in record:
            data = i["category"]
            data_str.append(data)
        result["data"] = data_str
        return jsonify(result), 200
    except:
        return jsonify({"erro": True, "message": "找不到任何訊息，伺服器錯誤"}), 500


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=3000)

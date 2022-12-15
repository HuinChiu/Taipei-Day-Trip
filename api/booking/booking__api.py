from flask import *
from mysql.connector import pooling
import ssl
import os
from dotenv import load_dotenv
import jwt

# 使用.env隱藏私密訊息
load_dotenv()
sql_user = os.getenv("sql_user")
sql_password = os.getenv("sql_password")

# 安全憑證
ssl._create_default_https_context = ssl._create_unverified_context

# 登入資mysql料庫
connection_pool = pooling.MySQLConnectionPool(
    pool_name="py_pool",
    pool_size=10,
    pool_reset_session=True,
    host="localhost",          # 主機名稱
    database="taipei_day_trip",  # 資料庫名稱
    user=sql_user,        # 帳號
    password=sql_password)  # 密碼


# 初始化blueprint
booking = Blueprint("booking", __name__)

# 設定jwt的密鑰
secret_key = os.getenv("secret_key")
booking.secret_key = secret_key


@booking.route("/api/booking", methods=["GET"])  # 取得景點列表
def get_booking_data():

    try:
        result = {"data": {"attraction": {"id": "", "name": "",
                                          "address": "", "image": "", }, "date": "", "time": "", "price": ""}}
        cookie = request.cookies
        token = cookie.get("token")
        print(token)
        if token == None:
            return jsonify({"erro": True, "message": "未登入系統，拒絕存取"}, 403)
        else:
            decode = jwt.decode(token, secret_key, algorithms=["HS256"])
            print(decode)
            email = decode["email"]
            connection_object = connection_pool.get_connection()
            cursor = connection_object.cursor(dictionary=True)
            query = ("SELECT id FROM members WHERE email=%s;")
            cursor.execute(query, (email,))
            record = cursor.fetchone()
            print(record)
            id = record["id"]
            query2 = ("SELECT attraction.id, attraction.name, attraction.address, attraction.images,date_format(orders.date,'%Y-%m-%d') , orders.time , orders.price FROM attraction INNER JOIN orders ON orders.attraction_id=attraction.id WHERE member_id=%s ORDER BY order_time DESC;")
            cursor.execute(query2, (id,))
            record2 = cursor.fetchone()
            print(record2)
            image = record2["images"].split(",")[0]
            print(image)
            result["data"]["attraction"]["id"] = record2["id"]
            result["data"]["attraction"]["name"] = record2["name"]
            result["data"]["attraction"]["address"] = record2["address"]
            result["data"]["attraction"]["image"] = image
            result["data"]["date"] = record2["date_format(orders.date,'%Y-%m-%d')"]
            result["data"]["time"] = record2["time"]
            result["data"]["price"] = record2["price"]
            print(result)

        return jsonify(result), 200

    except:
        return jsonify({"erro": True})


@ booking.route("/api/booking", methods=["POST"])
def create_booking_data():
    try:
        data = request.get_json()
        print(data)
        member_id = data["member_id"]
        attraction_id = data["attractionID"]
        date = data["date"]
        time = data["time"]
        price = data["price"]
        print(attraction_id, date, time, price)
        cookie = request.cookies
        token = cookie.get("token")
        if token == None:
            return jsonify({"erro": True, "message": "未登入系統，拒絕存取"}, 403)

        elif member_id == "" or attraction_id == "" or date == "" or time == "":
            return jsonify({"erro": True, "message": "輸入資料有誤，請重新點選"}, 400)

        else:
            connection_object = connection_pool.get_connection()
            cursor = connection_object.cursor(dictionary=True)
            query = (
                "INSERT INTO orders(member_id, attraction_id,date,time,price) VALUES ( %s, %s, %s, %s, %s);")
            cursor.execute(
                query, (member_id, attraction_id, date, time, price))
            connection_object.commit()
            cursor.close()
            connection_object.close()
            return jsonify({"ok": True})
    except:
        return jsonify({"error": True, "message": "伺服器錯誤"}), 500


@ booking.route("/api/booking", methods=["DELETE"])
def delete_booking_data():
    try:
        cookie = request.cookies
        token = cookie.get("token")
        if token != None:
            data = request.get_json()
            print(data)
            member_id = data["id"]
            attraction_id = data["attraction_id"]
            date = data["date"]
            time = data["time"]
            price = data["price"]
            print(member_id, attraction_id, date, time, price)
            connection_object = connection_pool.get_connection()
            cursor = connection_object.cursor(dictionary=True)
            query = (
                "DELETE FROM orders WHERE member_id=%s and attraction_id=%s and date=%s and time=%s and price=%s;")
            cursor.execute(
                query, (member_id, attraction_id, date, time, price))
            connection_object.commit()
            cursor.close()
            connection_object.close()
            return jsonify({"ok": True})
    except:
        return jsonify({"error": True, "message": "未登入系統，拒絕存取"}), 403

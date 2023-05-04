from flask import *
from mysql.connector import pooling
import ssl
import os
from dotenv import load_dotenv
import jwt
from mysql_connect import connection_pool

# 使用.env隱藏私密訊息
load_dotenv()
sql_user = os.getenv("sql_user")
sql_password = os.getenv("sql_password")

# 安全憑證
ssl._create_default_https_context = ssl._create_unverified_context

# 初始化blueprint
booking = Blueprint("booking", __name__)

# 設定jwt的密鑰
secret_key = os.getenv("secret_key")
booking.secret_key = secret_key
secretkey = os.getenv("jwt_secretkey")


@booking.route("/api/booking", methods=["GET"])  # 取得景點列表
def get_booking_data():
    # 連接資料庫
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor(dictionary=True)

    try:
        result = {"data": {"attraction": {"id": "", "name": "",
                                          "address": "", "image": "", }, "date": "", "time": "", "price": ""}}
        cookie = request.cookies
        token = cookie.get("token")
        decode = jwt.decode(token, secretkey, algorithms=["HS256"])
        if decode == None:
            return jsonify({"erro": True, "message": "未登入系統，拒絕存取"}, 403)
        else:

            id = decode["id"]
            query2 = ("SELECT attraction.id, attraction.name, attraction.address, "
                      "attraction.images,date_format(booking.date,'%Y-%m-%d') , booking.time ,"
                      " booking.price FROM attraction INNER JOIN booking ON "
                      "booking.attraction_id=attraction.id WHERE member_id=%s ORDER BY "
                      "order_time DESC;")
            cursor.execute(query2, (id,))
            record2 = cursor.fetchone()
            image = record2["images"].split(",")[0]
            result["data"]["attraction"]["id"] = record2["id"]
            result["data"]["attraction"]["name"] = record2["name"]
            result["data"]["attraction"]["address"] = record2["address"]
            result["data"]["attraction"]["image"] = image
            result["data"]["date"] = record2["date_format(booking.date,'%Y-%m-%d')"]
            result["data"]["time"] = record2["time"]
            result["data"]["price"] = record2["price"]
            return jsonify(result)

    except:
        return jsonify({"erro": True})
    finally:
        cursor.close()
        connection_object.close()
        print("booking get close")


@ booking.route("/api/booking", methods=["POST"])
def create_booking_data():
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor(dictionary=True)
    try:
        data = request.get_json()
        member_id = data["member_id"]
        attraction_id = data["attractionID"]
        date = data["date"]
        time = data["time"]
        price = data["price"]
        cookie = request.cookies
        token = cookie.get("token")
        decode = jwt.decode(token, secretkey, algorithms=["HS256"])
        if decode == None:
            return jsonify({"erro": True, "message": "未登入系統，拒絕存取"}, 403)
        elif member_id == "" or attraction_id == "" or date == "" or time == "":
            return jsonify({"erro": True, "message": "輸入資料有誤，請重新點選"}, 400)
        else:
            query = ("SELECT * FROM booking WHERE member_id=%s;")
            cursor.execute(query, (member_id,))
            member_data = cursor.fetchone()
            connection_object.commit()
            if member_data == None:
                query1 = (
                    "INSERT INTO booking(member_id, attraction_id,date,time,price) VALUES ( %s, %s, %s, %s, %s);")
                cursor.execute(
                    query1, (member_id, attraction_id, date, time, price))
                connection_object.commit()

                return jsonify({"ok": True})
            else:
                query2 = (
                    "DELETE FROM booking WHERE member_id=%s;")
                cursor.execute(
                    query2, (member_id,))
                connection_object.commit()
                query3 = (
                    "INSERT INTO booking(member_id, attraction_id,date,time,price) VALUES ( %s, %s, %s, %s, %s);")
                cursor.execute(
                    query3, (member_id, attraction_id, date, time, price))
                connection_object.commit()

                return jsonify({"ok": True})
    except:
        return jsonify({"error": True, "message": "伺服器錯誤"}), 500
    finally:
        cursor.close()
        connection_object.close()


@ booking.route("/api/booking", methods=["DELETE"])
def delete_booking_data():
    connection_object = connection_pool.get_connection()
    cursor = connection_object.cursor(dictionary=True)
    try:
        cookie = request.cookies
        token = cookie.get("token")
        decode = jwt.decode(token, secretkey, algorithms=["HS256"])
        if decode == None:
            return jsonify({"erro": True, "message": "未登入系統，拒絕存取"}, 403)
        else:
            data = request.get_json()
            member_id = data["id"]
            if decode["id"] != member_id:
                return jsonify({"erro": True, "message": "登入者不同，拒絕存取"}, 403)
            else:
                attraction_id = data["attraction_id"]
                date = data["date"]
                time = data["time"]
                price = data["price"]
                query = (
                    "DELETE FROM booking WHERE member_id=%s and attraction_id=%s and date=%s and time=%s and price=%s;")
                cursor.execute(
                    query, (member_id, attraction_id, date, time, price))
                connection_object.commit()

                return jsonify({"ok": True})
    except:
        return jsonify({"error": True, "message": "未登入系統，拒絕存取"}), 403
    finally:
        cursor.close()
        connection_object.close()

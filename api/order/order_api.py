from flask import *
from mysql.connector import pooling
import ssl
import os
from dotenv import load_dotenv
import requests
import datetime
import jwt
from mysql_connect import connection_pool
# 使用.env隱藏私密訊息
load_dotenv()
sql_user = os.getenv("sql_user")
sql_password = os.getenv("sql_password")
partner_key = os.getenv("partner_key")
merchant_id = os.getenv("merchant_id")
secretkey = os.getenv("jwt_secretkey")
# 安全憑證
ssl._create_default_https_context = ssl._create_unverified_context


# 初始化blueprint
orders = Blueprint("orders", __name__)


@ orders.route("/api/orders", methods=["POST"])
def pay_data():
    cookie = request.cookies
    token = cookie.get("token")
    decode = jwt.decode(token, secretkey, algorithms=["HS256"])
    if decode == None:
        return jsonify({"erro": True, "message": "未登入系統，拒絕存取"}, 403)
    url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
    try:
        data = request.get_json()
        print(data)
        if data["prime"] == "":
            return jsonify({"error": True, "message": "訂單建立失敗，付款失敗，請重新輸入"})
        # 建立訂單編號
        order_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # 建立訂單編號
        # 新增資料至後端
        member_email = data["contact"]["email"]
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor(dictionary=True)
        query_member_id = ("SELECT id from members WHERE email=%s;")
        cursor.execute(query_member_id, (member_email,))
        find_id = cursor.fetchone()
        member_id = find_id["id"]
        query_history = ("SELECT * FROM orders WHERE member_id=%s;")
        cursor.execute(query_history, (member_id,))
        find_history = cursor.fetchone()
        if find_history != None:
            delete_history = ("DELETE FROM orders WHERE member_id=%s;")
            cursor.execute(delete_history, (member_id,))
            connection_object.commit()
        member_name = data["contact"]["name"]
        member_phone = data["contact"]["phone"]
        order_price = data["order"]["price"]
        query = ("INSERT INTO orders(order_id,member_id,member_name,"
                 "member_email,member_phone,price,pay_status) VALUES(%s,%s,%s,%s,%s,%s,1);")
        cursor.execute(query, (order_id, member_id, member_name,
                               member_email, member_phone, order_price))
        connection_object.commit()
        post_data = {  # 建立傳送至第三方支付資料
            "prime": data["prime"],
            "partner_key": partner_key,
            "merchant_id": merchant_id,
            "details": "taipei-day-trip",
            "order_number": order_id,
            "amount": int(data["order"]["price"]),
            "cardholder": {
                "phone_number": data["contact"]["phone"],
                "name": data["contact"]["name"],
                "email": data["contact"]["email"]
            }
        }
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': partner_key
        }

        response = requests.post(url, headers=headers, json=post_data)
        record = response.json()
        if record["status"] == 0:
            final_status = 0
            change_status = (
                "update orders set pay_status = %s where order_id =%s;")
            cursor.execute(change_status, (final_status, order_id))
            connection_object.commit()
            result = {"data": {"number": "", "payment": {
                "status": "", "message": "付款成功"}}}
            result["data"]["number"] = order_id
            result["data"]["payment"]["status"] = final_status
            return jsonify(result), 200
        else:
            return jsonify({"error": True, "message": "訂單建立失敗，付款失敗，請重新輸入"}), 400

    except:
        return jsonify({"error": True, "message": "伺服器錯誤"}), 500
    finally:
        cursor.close()
        connection_object.close()


@ orders.route("/api/orders", methods=["GET"])
def get_pay_data():
    try:
        result = {"data": {
            "number": "",
            "price": "",
            "trip": {
                "attraction": {
                    "id": "",
                    "name": "",
                    "address": "",
                    "image": "",
                },
                "date": "",
                "time": ""
            },
            "contact": {
                "name": "",
                "email": "",
                "phone": ""
            },
            "status": ""
        }}
        cookie = request.cookies
        token = cookie.get("token")
        decode = jwt.decode(token, secretkey, algorithms=["HS256"])
        if decode == None:
            return jsonify({"erro": True, "message": "未登入系統，拒絕存取"}, 403)
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor(dictionary=True)
        id = decode["id"]
        email = decode["email"]
        query2 = ("SELECT attraction.id, attraction.name, attraction.address, attraction.images,date_format(booking.date,'%Y-%m-%d') , booking.time , booking.price FROM attraction INNER JOIN booking ON booking.attraction_id=attraction.id WHERE member_id=%s ORDER BY order_time DESC;")
        cursor.execute(query2, (id,))
        record2 = cursor.fetchone()
        image = record2["images"].split(",")[0]
        result["data"]["trip"]["attraction"]["id"] = record2["id"]
        result["data"]["trip"]["attraction"]["name"] = record2["name"]
        result["data"]["trip"]["attraction"]["address"] = record2["address"]
        result["data"]["trip"]["attraction"]["image"] = image
        result["data"]["trip"]["date"] = record2["date_format(booking.date,'%Y-%m-%d')"]
        result["data"]["trip"]["time"] = record2["time"]
        if record2 != None:
            query = ("SELECT * from orders WHERE member_email=%s;")
            cursor.execute(query, (email,))
            record = cursor.fetchone()
            result["data"]["contact"]["name"] = record["member_name"]
            result["data"]["contact"]["email"] = record["member_email"]
            result["data"]["contact"]["phone"] = record["member_phone"]
            result["data"]["number"] = record["order_id"]
            result["data"]["price"] = record["price"]
            result["data"]["status"] = record["pay_status"]
        return jsonify(result)
    except:
        return jsonify({"error": True, "message": "伺服器錯誤"}), 500
    finally:
        cursor.close()
        connection_object.close()
        print("orders close")

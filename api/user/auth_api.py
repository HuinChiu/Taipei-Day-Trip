from flask import *
from mysql.connector import pooling
import os
from dotenv import load_dotenv
import jwt
from jwt import exceptions
from datetime import datetime, timedelta

# 使用.env隱藏私密訊息
load_dotenv()
sql_user = os.getenv("sql_user")
sql_password = os.getenv("sql_password")

# 登入資mysql料庫
connection_pool = pooling.MySQLConnectionPool(
    pool_name="py_pool",
    pool_size=5,
    pool_reset_session=True,
    host="localhost",          # 主機名稱
    database="taipei_day_trip",  # 資料庫名稱
    user=sql_user,        # 帳號
    password=sql_password)  # 密碼


# 初始化blueprint
auth = Blueprint("auth", __name__)
# 設定jwt的密鑰
secret_key = os.getenv("secret_key")
auth.secret_key = secret_key
secretkey = os.getenv("jwt_secretkey")


@ auth.route("/api/user", methods=["POST"])
def signup():
    try:
        data = request.get_json()
        name = data["name"]
        email = data["email"]
        password = data["password"]
        if name == "" or email == "" or password == "":
            return jsonify({"erro": True, "message": "註冊失敗，資料未輸入完全，請重新輸入"})

        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor(dictionary=True)
        query = ("SELECT email FROM members WHERE email=%s")
        cursor.execute(query, (email,))
        record = cursor.fetchone()
        if record == None:
            query1 = (
                "INSERT INTO members(name, email, password)VALUES(%s, %s, %s);")
            value = (name, email, password)
            cursor.execute(query1, value)
            connection_object.commit()
            cursor.close()
            connection_object.close()
            return jsonify({"ok": True}), 200
        else:
            return jsonify({"erro": True, "message": "註冊失敗，email已被註冊，請重新輸入"}), 400
    except:
        return jsonify({"error": "true", "message": "伺服器錯誤"}), 500


@auth.route("/api/user/auth", methods=["PUT"])
def signin():
    try:
        data = request.get_json()
        email = data["email"]
        password = data["password"]
        if email == "" or password == "":
            return jsonify({"erro": True, "message": "登入失敗，資料未輸入完全，請重新輸入"})
        member = (email, password)
        connection_object = connection_pool.get_connection()
        cursor = connection_object.cursor(dictionary=True)
        query = ("SELECT * FROM members WHERE email=%s AND password=%s")
        cursor.execute(query, member)
        record = cursor.fetchone()
        cursor.close()
        connection_object.close()
        if record == None:
            return jsonify({"erro": True, "message": "登入失敗，帳號或密碼錯誤"})
        else:
            id=record["id"]
            name = record["name"]
            email = record["email"]
            payload = {
                "id":id,
                "username": name,
                "email": email,
                "exp": (datetime.utcnow() + timedelta(days=7))

            }
            token = jwt.encode(payload, secretkey, algorithm="HS256")
            response = make_response(jsonify({"ok": True}))
            response.set_cookie("token", value=token,
                                expires=datetime.utcnow() + timedelta(days=7))

            return response, 200
    except:
        return jsonify({"error": "true", "message": "伺服器錯誤"}), 500


@auth.route("/api/user/auth", methods=["GET"])
def getmemberdata():
    try:
        result = {"data": None}
        cookie = request.cookies
        token = cookie.get("token")
        if token == None:
            return jsonify({"data": None})
        else:
            decode = jwt.decode(token, secretkey, algorithms=["HS256"])
            user_name = decode["username"]
            email = decode["email"]
            connection_object = connection_pool.get_connection()
            cursor = connection_object.cursor(dictionary=True)
            query = ("SELECT id,name,email FROM members WHERE email=%s AND name=%s")
            cursor.execute(query, (email, user_name))
            record = cursor.fetchone()
            connection_object.close()
            cursor.close()
            result["data"] = record
        return jsonify(result)
    except exceptions.ExpiredSignatureError:
        return jsonify({"data": None})
    except jwt.DecodeError:
        return jsonify({"data": None})
    except jwt.InvalidTokenError:
        return jsonify({"data": None})


@ auth.route("/api/user/auth", methods=["DELETE"])
def signout():
    try:
        response = make_response(jsonify({"ok": True}))
        response.delete_cookie("token")
        return response, 200
    except:
        return jsonify({"error": "true", "message": "伺服器錯誤"}), 500

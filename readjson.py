import json
import os
from dotenv import load_dotenv
from mysql.connector import pooling
# 隱藏私密資料
load_dotenv()
sql_user = os.getenv("sql_user")
sql_password = os.getenv("sql_password")
# 登入mysql
connection_pool = pooling.MySQLConnectionPool(
    pool_name="py_pool",
    pool_size=5,
    pool_reset_session=True,
    host="localhost",          # 主機名稱
    database="taipei_day_trip",  # 資料庫名稱
    user=sql_user,        # 帳號
    password=sql_password)  # 密碼
# 讀取json檔案
jsonFile = open("data/taipei-attractions.json", "r", encoding="utf8")
data = json.load(jsonFile)
alldata = data["result"]["results"]
# 將各值取出加入列表
name_data = []
category_data = []
description_data = []
address_data = []
transport_data = []
mrt_data = []
lat_data = []
lng_data = []
images_data = []  # 景點的所有圖片
final_img_data = []  # 整理過後的圖片列表


for i in alldata:
    name = i["name"]
    name_data.append(name)
    category = i["CAT"]
    category_data.append(category)
    description = i["description"]
    description_data.append(description)
    address = i["address"]
    address_data.append(address)
    transport = i["direction"]
    transport_data.append(transport)
    mrt = i["MRT"]
    mrt_data.append(mrt)
    lat = i["latitude"]
    lat_data.append(lat)
    lng = i["longitude"]
    lng_data.append(lng)
    images = i["file"].lower()
    images_data.append(images)
category_data[20] = "其他"
num = len(images_data)

second_img_data = []
for i in range(num):  # 將img重新整理去掉mp3.flv檔案
    new_list = []
    data = images_data[i].split(".jpg")
    for j in data:
        if "mp3" in j:
            data.remove(j)
        elif "flv" in j:
            data.remove(j)
        elif j == "":
            data.remove(j)
    for k in data:
        k += ".jpg"
        new_list.append(k)
    second_img_data.append(new_list)  # 將所有圖片整理好後加入final_img_data
for i in second_img_data:
    symbol = ","
    all_img = symbol.join(i)
    final_img_data.append(all_img)

# 將每筆資料存入mysql arrraction
for i in range(num):
    connection_obj = connection_pool.get_connection()
    cursor = connection_obj.cursor()  # 使用游標
    sql = ("INSERT INTO attraction (name,category,description,address,transport,mrt,lat,lng,images)"
           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);")
    insert_data = (name_data[i], category_data[i], description_data[i], address_data[i], transport_data[i],
                   mrt_data[i], lat_data[i], lng_data[i], final_img_data[i])
    cursor.execute(sql, insert_data)
    connection_obj.commit()
    connection_obj.close()

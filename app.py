from flask import *
from api.attraction.attraction_api import attraction
from api.category.category_api import category
from api.user.auth_api import auth
from api.booking.booking_api import booking
from api.order.order_api import orders


# 初始化flask
app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/")
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['JSON_SORT_KEYS'] = False

# 註冊blueprint
app.register_blueprint(attraction)
app.register_blueprint(category)
app.register_blueprint(auth)
app.register_blueprint(booking)
app.register_blueprint(orders)


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


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=3000)  # , ssl_context='adhoc')

from API_Flask.API.Web.Lib import Weather_API
from flask import Flask, render_template
app = Flask(__name__)
cities_list = [
    "Ho Chi Minh",
    "Thua Thien Hue",
    "Ha Noi",
    "Da Nang"
]


@app.route("/", methods=["GET"])
@app.route("/<string:location>", methods=["GET"])
def api_get_weather_info(location=cities_list[0]):
    info_json = Weather_API.get_info(location)
    # .html file must be contained in folder "templates" name (required)
    return render_template('Weather.html', info_json=info_json, cities_list=cities_list, selected_city=location)


if __name__ == '__main__':
    app.run(debug=True)
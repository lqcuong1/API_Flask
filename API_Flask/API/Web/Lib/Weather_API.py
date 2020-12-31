import requests
# current day + next 2 days (max)
num_day_forecast = 3


def get_info(location):
    info_json = {
        "current": {
            "location": "",
            "country": "",
            "lat - lon": "",
            "last-updated": "",
            "request_time": "",
            "temperature": "",
            "description": "",
            "icon": "",
            "humidity": "",
            "uv_index": "",
        },
        "forecast": []
    }
    try:
        url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
        querystring = {
            "q": location,
            "days": num_day_forecast
        }
        headers = {
            'x-rapidapi-key': "269f38f00emshbddd98e513945e9p1efae6jsne54fced8b127",
            'x-rapidapi-host': "weatherapi-com.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == 200:
            obj = response.json()

            # current
            info_json["current"]["location"] = obj["location"]["name"]
            info_json["current"]["country"] = obj["location"]["country"]
            info_json["current"]["request_time"] = obj["location"]["localtime"]
            info_json["current"]["lat - lon"] = str(obj["location"]["lat"]) + "° - " + str(obj["location"]["lon"]) + "°"
            info_json["current"]["last-updated"] = obj["current"]["last_updated"]
            info_json["current"]["temperature"] = str(obj["current"]["temp_c"]) + "°C"
            info_json["current"]["description"] = obj["current"]["condition"]["text"]
            info_json["current"]["icon"] = obj["current"]["condition"]["icon"]
            info_json["current"]["humidity"] = str(obj["current"]["humidity"]) + "%"
            info_json["current"]["uv_index"] = str(obj["current"]["uv"]) + " - " + get_status_uv(obj["current"]["uv"])

            # forecast
            for index in range(1, num_day_forecast):
                obj_forecast = obj["forecast"]["forecastday"][index]
                info_json["forecast"].append({
                    "date": obj_forecast["date"],
                    "temperature": str(obj_forecast["day"]["mintemp_c"]) + "°C - " + str(obj_forecast["day"]["maxtemp_c"]) + "°C",
                    "uv_index": str(obj_forecast["day"]["uv"]) + " - " + get_status_uv(obj_forecast["day"]["uv"]),
                    "chance_of_rain": str(obj_forecast["day"]["daily_chance_of_rain"]) + "%",
                    "total_precipitation": str(obj_forecast["day"]["totalprecip_mm"]) + "mm",
                    "average_humidity": str(obj_forecast["day"]["avghumidity"]) + "%",
                    "description": obj_forecast["day"]["condition"]["text"],
                    "icon": obj_forecast["day"]["condition"]["icon"],
                })

    except Exception as e:
        print("Error! ", e)
    return info_json


def get_status_uv(uv_str):
    uv_value = int(uv_str)
    if uv_value <= 2:
        return "LOW"
    elif uv_value <= 5:
        return "MODERATE"
    elif uv_value <= 7:
        return "HIGH"
    elif uv_value <= 10:
        return "VERY HIGH"
    else:
        return "EXTREME"

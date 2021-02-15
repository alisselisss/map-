import requests
import json


def get_params(toponym_to_find, z):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        print("Ошибка выполнения запроса:")
        print(geocoder_api_server)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]

    size = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]["boundedBy"]["Envelope"]

    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:

    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    arg1 = size['lowerCorner'].split()
    arg2 = size['upperCorner'].split()
    a, b = float(arg1[0]), float(arg1[1])
    c, d = float(arg2[0]), float(arg2[1])

    delta1 = abs(c - a)
    delta2 = abs(d - b)


    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "z": f'{z}',
        "l": "map",
        "pt": f"{toponym_longitude},{toponym_lattitude}"
    }
    return map_params
import sys
# Этот класс поможет нам сделать картинку из потока байт

import requests
import pygame

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

delta = "0.005"
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([delta, delta]),
    "l": "map"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
width, height = 700, 500
screen = pygame.display.set_mode((width, height))
pygame.display.flip()

running = True
while running:
    screen.blit(pygame.image.load(map_file), (0, 0))
    for i in pygame.event.get():
        if pygame.event.wait().type == pygame.QUIT:
            running = False
    pygame.display.flip()
pygame.quit()
import sys
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт
from wwwwwww import get_params
import requests
import pygamei

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

z = 12

# Собираем параметры для запроса к StaticMapsAPI:
map_params = get_params(toponym_to_find, z)

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.flip()

running = True
while running:
    screen.blit(pygame.image.load(map_file), (0, 0))
    for i in pygame.event.get():
        if pygame.event.wait().type == pygame.QUIT:
            running = False
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_PAGEUP:    # прокручивание вперёд
                if z < 17:
                    z += 1
                    map_params = get_params(toponym_to_find, z)
                    response = requests.get(map_api_server, params=map_params)
                    map_file = "map.png"

            if i.key == pygame.K_PAGEDOWN:   # прокручивание назад
                if z > 1:
                    z -= 1
                    map_params = get_params(toponym_to_find, z)
                    response = requests.get(map_api_server, params=map_params)
                    map_file = "map.png"
            with open(map_file, "wb") as file:
                file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()
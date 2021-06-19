import sys
from io import BytesIO
import requests
from PIL import Image
import pygame


def index(address):
    try:
        geocoder_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={' '.join(address)}, 1&format=json"
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            toponym_coodrinates = toponym["Point"]["pos"]
            # city = json_response["response"]["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]["request"]
            return json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
    except:
        return 'Ошибка почтового индекса. Проверьте адрес'

def search(inp, delta, screen, l, *again):
    global old_inp, toponym_longitude, toponym_lattitude, old_coords
    if again:
        inp = 'Москва'.split()
        toponym_to_find = " ".join(inp)
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params)
        if not response:
            pass
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        old_coords = [toponym_longitude, toponym_lattitude]
    if inp != old_inp:

        old_inp = inp
        delta = "11"
        toponym_to_find = " ".join(inp)
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params)
        if not response:
            pass
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        old_coords = [toponym_longitude, toponym_lattitude]

    response = requests.get(f"https://static-maps.yandex.ru/1.x/?l={l}&ll={toponym_longitude},{toponym_lattitude}&pt={old_coords[0]},{old_coords[1]},pm2rdm,org&z={delta}")
    image = Image.open(BytesIO(
        response.content))
    image.save('file.png')
    a = pygame.image.load('file.png')
    b = a.get_rect(bottomright=(600, 600))
    screen.blit(a, b)


def geocode(address):
    global toponym_longitude, toponym_lattitude
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        pass
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return toponym_longitude, toponym_lattitude

old_inp = ''
l = 'map'
inp = 'Москва'.split()
delta = "11"
toponym_to_find = " ".join(inp)
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}
response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    pass
json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
old_coords = [toponym_longitude, toponym_lattitude]


if __name__ == '__main__':
    running = True
    pygame.init()
    size = width, height = 600, 600
    pygame.display.set_caption('page')
    screen = pygame.display.set_mode(size)
    screen.fill((255, 204, 0))
    search(inp, delta, screen, l)
    font = pygame.font.Font(None, 32)
    input_box = pygame.Rect(10, 60, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    txt_surface = font.render(text, True, color)
    button = pygame.Rect(415, 10, 180, 60)

    txt4a = True
    pygame.display.flip()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position

                # checks if mouse position is over the button

                if button.collidepoint(mouse_pos):
                    # prints current location of mouse
                    print('button was pressed at {0}'.format(mouse_pos))
                    if txt4a:
                        txt4a = False
                    else:
                        txt4a = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        inp = text.split()
                        text = ''
                        search(inp, delta, screen, l)
                        screen.fill((255, 204, 0))
                        search(inp, delta, screen, l)
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        screen.fill((255, 204, 0))
                        search(inp, delta, screen, l)
                    else:
                        text += event.unicode

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not active:
                if l == 'map':
                    l = 'sat'
                else:
                    l = 'map'
                search(inp, delta, screen, l)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
                if float(delta) < 17:
                    delta = str(int(delta) + 1)
                    search(inp, delta, screen, l)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEUP:
                if float(delta) > 1:
                    delta = str(int(delta) - 1)
                    search(inp, delta, screen, l)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:

                toponym_longitude = str(float(toponym_longitude) + 0.05 / float(delta))[0:10]
                search(inp, delta, screen, l)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:

                toponym_longitude = str(float(toponym_longitude) - 0.05 / float(delta))[0:10]
                search(inp, delta, screen, l)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:

                toponym_lattitude = str(float(toponym_lattitude) + 0.05 / float(delta))[0:10]
                search(inp, delta, screen, l)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:

                toponym_lattitude = str(float(toponym_lattitude) - 0.05 / float(delta))[0:10]
                search(inp, delta, screen, l)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                inp, delta = 'Москва'.split(), "11"
                search(inp, delta, screen, l, True)



            txt_surface = font.render(text, True, color)
            screen.blit(txt_surface, (15, 63))
            pygame.display.flip()
            width = 400
            input_box.w = width
            #screen.blit(txt_surface, (10, 50))
            pygame.draw.rect(screen, color, input_box, 2)


            f = pygame.font.SysFont('arial', 18)
            txt = f.render('Для переключения слоев карты нажмите пробел', True, (255, 0, 0))
            txt1 = f.render('Для окончания ввода точки поиска нажмите Enter', True, (255, 0, 0))
            txt2 = f.render('Для сброса поиска нажмите Escape', True, (255, 0, 0))
            txt3 = f.render(f'Найденный объект - {inp[0] if len(inp) == 1 else inp}', True, (255, 0, 0))
            txt4 = f.render('П. индекс - Вкл', True, (5, 0, 0))
            txt5 = f.render('П. индекс - Выкл', True, (5, 0, 0))
            txt6 = f.render(f'{index(inp)}', True, (5, 0, 0))
            screen.blit(txt, (10, 10))
            screen.blit(txt1, (10, 30))
            screen.blit(txt2, (10, 100))
            screen.blit(txt3, (10, 127))

            pygame.draw.rect(screen, [255, 0, 0], button)
            if txt4a:
                screen.blit(txt4, (420, 10))
                screen.blit(txt6, (420, 30))

            else:
                screen.blit(txt5, (420, 10))
                pygame.display.flip()

        pygame.display.flip()
    pygame.quit()



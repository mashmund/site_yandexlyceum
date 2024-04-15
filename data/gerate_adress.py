import requests
import folium


def generate_map_with_address(address, x1, x2):
    m = folium.Map(location=[x2, x1], zoom_start=100)  # Центрируем карту по определенным координатам
    folium.Marker([x2, x1], popup=address).add_to(m)  # Добавляем маркер с указанным адресом

    map_html = m._repr_html_()  # Получаем HTML код карты

    return map_html


def get_coordinates_by_address(address):
    url = f'https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&format=json&geocode={address}'
    response = requests.get(url)
    data = response.json()

    try:
        coordinates = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        coordinates = tuple(map(float, coordinates.split()))
        return coordinates
    except (KeyError, IndexError):
        return None


def get_adress(address):
    a = get_coordinates_by_address(address)
    return generate_map_with_address(address, a[0], a[1])


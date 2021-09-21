import requests
from rx import create
from rx.core import Observer

API_TOKEN = 'lmao-no'


class FilmRenderer(Observer):
    def on_next(self, film: dict) -> None:
        if film['Type'] != 'movie':
            return
        print(f'{film["imdbID"][2:]} - {film["Title"]}: {film["Poster"]}')

    def on_completed(self) -> None:
        print('Fin!')


def observer_teclado(observer, scheduler):
    while True:
        title = input('Introduce un título para buscar: ')
        if not title:
            break

        params = {'apikey': API_TOKEN, 't': title}
        content = requests.get('http://www.omdbapi.com/', params=params).json()

        if isinstance(content, list):
            for film in content['Search']:
                observer.on_next(film)
        else:
            observer.on_next(content)

        observer.on_completed()


observable = create(observer_teclado)
observable.subscribe(FilmRenderer())

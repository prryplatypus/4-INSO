import requests
from rx import from_, operators
from rx.core import Observer

API_TOKEN = 'lmao-no'


class FilmRenderer(Observer):
    def on_next(self, film: str) -> None:
        print(film)


params = {
    'apikey': API_TOKEN,
    's': input('Introduce un título para buscar: ')
}
content = requests.get('http://www.omdbapi.com/', params=params).json()

from_(content['Search']).pipe(
    operators.filter(lambda f: f['Type'] == 'movie'),
    operators.map(lambda f: f'{f["imdbID"][2:]} - {f["Title"]}: {f["Poster"]}'),
).subscribe(FilmRenderer())

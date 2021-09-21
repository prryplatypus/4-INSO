from rx import create
from rx.core import Observer


class Printer(Observer):
    def on_next(self, value) -> None:
        print(f'Recibido: {value}')

    def on_completed(self) -> None:
        print('Fin!')


def observer_teclado(observer, scheduler):
    while True:
        msg = input('Introduce una mensaje: ')
        if not msg:
            observer.on_completed()
            return
        observer.on_next(msg)


observable = create(observer_teclado)
observable.subscribe(Printer())

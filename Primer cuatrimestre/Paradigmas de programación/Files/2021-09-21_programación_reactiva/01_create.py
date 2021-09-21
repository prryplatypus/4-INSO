from rx import create


def generador(observer, scheduler):
    observer.on_next('Hola')
    observer.on_next('Adiós')
    observer.on_completed()


observable = create(generador)
observable.subscribe(
    on_next=lambda v: print(f'Recibido {v}')
)

from rx import of


observable = of('Hola', 'Adiós')
observable.subscribe(
    on_next=lambda v: print(f'Recibido {v}')
)

of('Hola', 'Adiós').subscribe(
    on_next=lambda v: print(f'Recibido {v}'),
    on_completed=lambda: print('Fin')
)

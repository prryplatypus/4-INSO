from rx import from_

el = [1, 2, 3, 4, 5]
observable = from_(el)

observable.subscribe(
    on_next=lambda v: print(f'Recibido {v}'),
    on_completed=lambda: print('Fin'),
    on_error=lambda e: print(f'Error: {e}')
)

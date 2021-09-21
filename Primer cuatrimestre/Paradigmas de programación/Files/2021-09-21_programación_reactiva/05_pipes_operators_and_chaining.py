from rx import of, operators


fuente = of('Hola', 'Adiós')

cadena = fuente.pipe(
    operators.map(lambda x: x.upper()),
    operators.map(lambda x: f'En mayúsculas: {x}')
)

cadena.subscribe(lambda x: print(f'Recibido: {x}'))

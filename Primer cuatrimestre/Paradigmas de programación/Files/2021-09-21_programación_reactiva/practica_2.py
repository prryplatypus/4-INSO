from functools import reduce
from itertools import permutations
from random import randint
from typing import List, Iterator

###############################################################################


def es_palindromo(palabra: str) -> bool:
    return palabra[::-1] == palabra


letras = "aabb"
print("Palindromos:")
for permutation in permutations(letras):
    permutation = "".join(permutation)
    print(f"\t- {permutation}: {es_palindromo(permutation)}")


###############################################################################


def impares_de(inicial: List[int]) -> Iterator[int]:
    return filter(lambda x: x % 2, inicial)


numeros = [randint(1, 100) for _ in range(0, 10)]
print("Impares:")
print(f"\t- Iniciales: {numeros}")
print(f"\t- Filtrados: {list(impares_de(numeros))}")


###############################################################################


def cuadrados_sumados(n: int) -> int:
    return sum(map(lambda x: x ** 2, range(1, n + 1)))


numeros = [randint(1, 100) for _ in range(0, 10)]
print("Cuadrados sumados:")
for num in numeros:
    print(f"\t- {num}: {cuadrados_sumados(num)}")


###############################################################################


def factorial(n: int) -> int:
    return reduce(lambda x, y: x * y, range(1, n + 1))


numeros = [randint(1, 10) for _ in range(0, 5)]
print("Factoriales:")
for num in numeros:
    print(f"\t- {num}: {factorial(num)}")


###############################################################################


def is_primo(n: int) -> bool:
    return n > 1 and all(n % i for i in range(2, n))


print("Primo:")
for num in range(1, 11):
    print(f"\t- {num}: {is_primo(num)}")


###############################################################################

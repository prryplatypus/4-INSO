## Principios (¡importante para examen!)

- Simplicidad: Los mecanismos de seguridad deben ser tan simples como sea posible. La complejidad es la raíz de muchos problemas de seguridad.
- Fail-Safe: Si ocurre un fallo, el sistema debe fallar de manera segura. Es decir, que los controles de seguridad y las configuraciones deben seguir funcionando.
- Mediación completa: En lugar de proporcionar acceso directo a la información, se mediadores deben emplear una política de acceso. Los ejemplos comunes de mediadores incluyen permisos del sistema de archivos, proxies, firewalls y pasarela de correo.
- Diseño abierto: La seguridad del sistema no debe depender del secreto de la implementación o sus componentes.
- Separación de privilegios: las funciones, en la medida de lo posible, deben estar separadas y proporcionar tanta granularidad como sea posible. Puede aplicarse tanto a sistemas como a operadores y usuario.
- Privilegio mínimo: Cada usuario debe tener concedidos el mínimo conjunto de derechos necesarios para realizar su trabajo.
- Aceptabilidad psicológica: Los usuarios deben comprender la necesidad de seguridad.
- Selección del mecanismo menos común: Cuando se proporciona una función para el sistema, es mejor tener un proceso o servicio que proporcione alguna función sin otorgar esa misma función a otras partes del sistema. Por ejemplo, que un servidor web pueda acceder a una BB.DD. no quiere decir que el resto de apps en el mismo sistema deban también poder acceder a ella.
- Defensa en profundidad: Un único mecanismo de seguridad es insuficiente. Deben estar en capas para que el compromiso de un sólo mecanismo no afecte a otras medidas.
- Factor de trabajo: Se debe comprender lo que se necesitaría para romper el sistema o la red, haciendo que la cantidad de trabajo necesaria exceda el valor que el atacante obtendría.
- Registros: Deben mantenerse de modo que, si se produce un ataque, la evidencia del ataque está disponible para la organización.

## Teorema de Bayes

[...]

## Matriz de confusión

- Accuracy = (TruePositive + TrueNegative) / (TruePositive + TrueNegative + FalsePositive + FalseNegative)
- Recall = TP / (TP + FN)
- Precision = TP / (TP + FP)

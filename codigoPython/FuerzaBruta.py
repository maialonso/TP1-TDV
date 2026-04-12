#Cambios necesarios:
#El único cambio estructural necesario: mejorEnergia en C++ es double& (referencia modificable). 
#En Python los floats son inmutables, así que lo envolví en una lista de un elemento (mejorEnergia[0]) para replicar exactamente ese comportamiento.
#La lógica es idéntica.



# función recursiva
def encontrarSeamFuerzaBrutaRec(energia: list[list[float]], i: int, j: int, n: int, m: int, S: list[int], B: list[int], energiaActual: float, mejorEnergia: list[float]) -> None:
    if i == n:              # caso base: es el final de la imagen
        if not B or energiaActual < mejorEnergia[0]:        # si encontró un camino mejor actualiza y guarda ese camino
            mejorEnergia[0] = energiaActual
            B[:] = S[:]
        return

    if j > 0:               # baja por la rama izquierda siempre y cuando no esté en un borde
        S.append(j - 1)
        encontrarSeamFuerzaBrutaRec(energia, i + 1, j - 1, n, m, S, B, energiaActual + energia[i][j - 1], mejorEnergia)
        S.pop()

    S.append(j)             # en todos los casos baja por la rama del medio
    encontrarSeamFuerzaBrutaRec(energia, i + 1, j, n, m, S, B, energiaActual + energia[i][j], mejorEnergia)
    S.pop()

    if j < m - 1:           # baja por la rama derecha siempre y cuando no esté en un borde
        S.append(j + 1)
        encontrarSeamFuerzaBrutaRec(energia, i + 1, j + 1, n, m, S, B, energiaActual + energia[i][j + 1], mejorEnergia)
        S.pop()

  # función principal
def encontrarSeamFuerzaBruta(energia: list[list[float]]) -> list[int]:
    if not energia:
        return []

    n = len(energia)        # filas
    m = len(energia[0])     # columnas

    B = []                          # mejor camino encontrado
    mejorEnergia = [float('inf')]

    for j in range(m):      # comenzando desde cada columna posible en la primer fila
        S = []
        S.append(j)
        encontrarSeamFuerzaBrutaRec(energia, 1, j, n, m, S, B, energia[0][j], mejorEnergia)
    
    return B

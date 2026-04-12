# cambios:
# el único cambio estructural: std::pair<std::vector<int>, double> no existe en Python, así que lo reemplacé por una lista de dos elementos [lista, float]



# función recursiva
def encontrarSeamBacktrackingRec(energia: list[list[float]], i: int, j: int, n: int, m: int, S: list, B: list) -> None:
    if i == n:                                          # caso base: es el final de la imagen
        if not B[0] or S[1] < B[1]:                    # si encontró un camino mejor actualiza y guarda ese camino
            B[0] = S[0][:]
            B[1] = S[1]
        return

    if S[1] < B[1]:                         # poda: solo sigue si el camino actual es mejor que el mejor conocido

        if j > 0:                           # baja por la izquierda siempre y cuando no esté en un borde
            S[0].append(j - 1)
            S[1] += energia[i][j - 1]
            encontrarSeamBacktrackingRec(energia, i + 1, j - 1, n, m, S, B)
            S[1] -= energia[i][j - 1]
            S[0].pop()

        S[0].append(j)                      # en todos los casos baja por la rama del medio
        S[1] += energia[i][j]
        encontrarSeamBacktrackingRec(energia, i + 1, j, n, m, S, B)
        S[1] -= energia[i][j]
        S[0].pop()

        if j < m - 1:                       # baja por la rama derecha siempre y cuando no esté en un borde
            S[0].append(j + 1)
            S[1] += energia[i][j + 1]
            encontrarSeamBacktrackingRec(energia, i + 1, j + 1, n, m, S, B)
            S[1] -= energia[i][j + 1]
            S[0].pop()

    else:
        return


# función principal
def encontrarSeamBacktracking(energia: list[list[float]]) -> list[int]:
    if not energia or not energia[0]:
        return []

    n = len(energia)                # filas
    m = len(energia[0])             # columnas

    B = [[], float('inf')]          # mejor camino encontrado

    for j in range(m):              # comenzando desde cada columna posible en la primer fila
        S = [[], 0.0]
        S[0].append(j)
        S[1] = energia[0][j]
        encontrarSeamBacktrackingRec(energia, 1, j, n, m, S, B)

    return B[0]

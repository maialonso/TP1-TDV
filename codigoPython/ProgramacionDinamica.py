# cambios:
# std::pair<int, double> lo reemplacé por una lista de dos elementos [int, float]

# función recursiva
def encontrarSeamPDRec(energia: list[list[float]], i: int, j: int, n: int, m: int, memo: list[list[list]]) -> list:
    if memo[i][j][1] != float('inf'):               # si ya resolvió este subproblema reutiliza el resultado (memorización)
        return memo[i][j]

    if i == 0:                          # caso base: está en la primera fila
        res = [j, energia[i][j]]        # dejamos como invariante que los casos base se tienen a si mismos
        memo[i][j] = res
        return res

    # definimos un min para comparaciones
    min_ = [-1, float('inf')]
    # definimos un mejor donde guardamos la posicion del mejor
    mejor = -1

    if j > 0 and j < m - 1:                     # si no está en un borde
        for k in range(j - 1, j + 2):           # recursión por {j-1, j, j+1}
            aux = encontrarSeamPDRec(energia, i - 1, k, n, m, memo)
            if min_[1] > aux[1]:                 # compara energías
                min_ = aux[:]
                mejor = k

    elif j == 0:                                # si está en la primer columna a la izquierda
        for k in range(j, j + 2):              # recursión por {j, j+1}
            aux = encontrarSeamPDRec(energia, i - 1, k, n, m, memo)
            if min_[1] > aux[1]:
                min_ = aux[:]
                mejor = k

    else:                                       # si está en la última columna a la derecha
        for k in range(j - 1, j + 1):          # recursión por {j-1, j}
            aux = encontrarSeamPDRec(energia, i - 1, k, n, m, memo)
            if min_[1] > aux[1]:
                min_ = aux[:]
                mejor = k

    min_[0] = mejor             # guarda la posición del elemento de donde vino
    min_[1] += energia[i][j]    # suma la energia acumulada hasta ahí
    memo[i][j] = min_            # actualiza memo
    return memo[i][j]


# funcion para invertir la solución dado que en la reconstrucción queda como primer posición el último elemento del camino
def invertirPairs(aInvertir: list[int]) -> list[int]:
    res = []
    for i in range(len(aInvertir) - 1, -1, -1):    # devuelve el vector en orden (primer elemento el primer elemento del camino)
        res.append(aInvertir[i])
    return res


# función que arma un vector del camino de la costura óptima
def reconstruccion(energia: list[list[float]], memo: list[list[list]], colInicio: int) -> list[int]:
    j = colInicio               # columna con menor energía acumulada
    respuesta = []
    respuesta.append(colInicio)
    for i in range(len(energia) - 1, 0, -1):        # empieza en la última fila
        posAnterior = memo[i][j][0]     # valor de la pos del elemento anterior
        respuesta.append(posAnterior)
        j = posAnterior                 # actualiza la columna en donde estoy

    res = invertirPairs(respuesta)      # llamado a la función que invierte la solución
    return res


# función principal
def encontrarSeamPD(energia: list[list[float]]) -> list[int]:
    if not energia or not energia[0]:
        return []

    # creo el memo
    n = len(energia)        # filas
    m = len(energia[0])     # columnas
    memo = [[[-1, float('inf')] for _ in range(m)] for _ in range(n)]  # memo = vector de vectores [int: columna "de dónde viene la mejor costura", double: energía acumulada]

    # se hace un llamado de la auxiliar por columna
    for j in range(m):
        encontrarSeamPDRec(energia, n - 1, j, n, m, memo)

    min_ = memo[n - 1][0][:]        # toma al elemento de la primer columna de la última fila como min para empezar
    pos = 0                         # guarda la posición con la que luego querrá reconstruir el camino
    for i in range(1, m):
        if min_[1] > memo[n - 1][i][1]:
            min_ = memo[n - 1][i][:]
            pos = i

    posColumna = reconstruccion(energia, memo, pos)     # reconstruye camino de la costura
    return posColumna

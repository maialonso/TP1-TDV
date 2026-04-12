#Cambios necesarios:
#el for de parseo de argumentos de C++ usa i++ dentro del loop, lo reemplacé por un while con i += 1


import sys
from FuerzaBruta import encontrarSeamFuerzaBruta
from Backtracking import encontrarSeamBacktracking
from ProgramacionDinamica import encontrarSeamPD
from Imagen import Imagen

# Lee una matriz de energía desde un archivo de texto.
# Formato esperado:
#   filas columnas
#   e00 e01 e02 ...
#   e10 e11 e12 ...
#   ...
def leerMatrizEnergia(ruta: str) -> list[list[float]]:
    with open(ruta, 'r') as archivo:
        if not archivo:
            raise RuntimeError("No se pudo abrir: " + ruta)

        primera_linea = archivo.readline().split()
        filas = int(primera_linea[0])
        columnas = int(primera_linea[1])

        energia = [[0.0] * columnas for _ in range(filas)]
        for f in range(filas):
            linea = archivo.readline().split()
            for c in range(columnas):
                energia[f][c] = float(linea[c])

    return energia


# Ejecuta el algoritmo seleccionado y devuelve el seam encontrado
def ejecutarAlgoritmo(energia: list[list[float]], algoritmo: str) -> list[int]:
    if algoritmo == "fb":   return encontrarSeamFuerzaBruta(energia)
    if algoritmo == "bt":   return encontrarSeamBacktracking(energia)
    if algoritmo == "pd":   return encontrarSeamPD(energia)
    raise RuntimeError("Algoritmo desconocido: " + algoritmo + ". Usar fb, bt o pd.")


def imprimirMatriz(matriz: list[list[float]]) -> None:
    for fila in matriz:
        for val in fila:
            print(val, end="\t")
        print()


def imprimirSeam(seam: list[int], energia: list[list[float]]) -> None:
    print("Seam encontrado: ", end="")
    total = 0.0
    for f in range(len(seam)):
        print(f"({f},{seam[f]})", end=" ")
        total += energia[f][seam[f]]
    print(f"\nEnergía total: {total}")


def modoNumerico(rutaEntrada: str, algoritmo: str) -> None:
    energia = leerMatrizEnergia(rutaEntrada)

    print("Matriz de energía:")
    imprimirMatriz(energia)
    print()

    seam = ejecutarAlgoritmo(energia, algoritmo)
    imprimirSeam(seam, energia)

    rutaSalida = "output/numericos/seam_" + algoritmo + ".txt"
    with open(rutaSalida, 'w') as salida:
        if salida:
            for f in range(len(seam)):
                salida.write(f"fila {f} -> columna {seam[f]}\n")
            print("Resultado guardado en " + rutaSalida)


def modoImagen(rutaImagen: str, algoritmo: str, iteraciones: int) -> None:
    img = Imagen(rutaImagen)
    print(f"Imagen cargada: {img.ancho()}x{img.alto()} px")

    for i in range(iteraciones):
        seam = ejecutarAlgoritmo(img.obtenerMatrizEnergia(), algoritmo)
        img.eliminarSeam(seam)

        if (i + 1) % 10 == 0 or i == iteraciones - 1:
            print(f"Iteración {i + 1}/{iteraciones} - Ancho actual: {img.ancho()} px")

    rutaSalida = "output/imagenes/resultado_" + algoritmo + ".png"
    img.guardar(rutaSalida)
    print("Imagen guardada en " + rutaSalida)


def imprimirUso() -> None:
    print("Uso:\n"
          "  Modo numérico: python seam.py --numerico <archivo> --algoritmo <fb|bt|pd>\n"
          "  Modo imagen:   python seam.py --imagen <archivo> --algoritmo <fb|bt|pd> --iteraciones <N>\n"
          "\nEjemplos:\n"
          "  python seam.py --numerico input/ejemplo.txt --algoritmo pd\n"
          "  python seam.py --imagen img/foto.jpg --algoritmo pd --iteraciones 50\n")


def main() -> int:
    if len(sys.argv) < 2:
        imprimirUso()
        return 1

    modo = ""
    rutaArchivo = ""
    algoritmo = "pd"
    iteraciones = 1

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--numerico" and i + 1 < len(sys.argv):
            modo = "numerico"
            i += 1
            rutaArchivo = sys.argv[i]
        elif arg == "--imagen" and i + 1 < len(sys.argv):
            modo = "imagen"
            i += 1
            rutaArchivo = sys.argv[i]
        elif arg == "--algoritmo" and i + 1 < len(sys.argv):
            i += 1
            algoritmo = sys.argv[i]
        elif arg == "--iteraciones" and i + 1 < len(sys.argv):
            i += 1
            iteraciones = int(sys.argv[i])
        elif arg == "--ayuda" or arg == "--help":
            imprimirUso()
            return 0
        i += 1

    try:
        if modo == "numerico":
            modoNumerico(rutaArchivo, algoritmo)
        elif modo == "imagen":
            modoImagen(rutaArchivo, algoritmo, iteraciones)
        else:
            imprimirUso()
            return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

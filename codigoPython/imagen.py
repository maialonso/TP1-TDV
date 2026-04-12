# cambios:
# stb_image es una librería C de carga/escritura de imágenes, la reemplacé por Pillow (PIL) que es su equivalente directo en Python.


from PIL import Image as PILImage
import math


class Imagen:

    def __init__(self, ruta: str = None):
        self._ancho = 0
        self._alto = 0
        self._pixeles = []
        if ruta is not None:
            self.cargar(ruta)

    def cargar(self, ruta: str) -> None:
        img = PILImage.open(ruta).convert("RGB")
        self._ancho = img.width
        self._alto = img.height

        self._pixeles = [[[0] * 3 for _ in range(self._ancho)] for _ in range(self._alto)]
        datos = img.tobytes()
        for f in range(self._alto):
            for c in range(self._ancho):
                idx = (f * self._ancho + c) * 3
                self._pixeles[f][c][0] = datos[idx]
                self._pixeles[f][c][1] = datos[idx + 1]
                self._pixeles[f][c][2] = datos[idx + 2]

    def guardar(self, ruta: str) -> None:
        if self.estaVacia():
            raise RuntimeError("La imagen está vacía.")

        datos = bytearray(self._alto * self._ancho * 3)
        for f in range(self._alto):
            for c in range(self._ancho):
                idx = (f * self._ancho + c) * 3
                datos[idx]     = self._pixeles[f][c][0]
                datos[idx + 1] = self._pixeles[f][c][1]
                datos[idx + 2] = self._pixeles[f][c][2]

        # Detectar formato por extensión
        ext = ruta[ruta.rfind('.') + 1:].lower()

        img = PILImage.frombytes("RGB", (self._ancho, self._alto), bytes(datos))

        if ext == "png":
            img.save(ruta, format="PNG")
        elif ext == "jpg" or ext == "jpeg":
            img.save(ruta, format="JPEG", quality=90)
        elif ext == "bmp":
            img.save(ruta, format="BMP")
        else:
            raise RuntimeError("Formato no soportado: " + ext + ". Usar .png, .jpg o .bmp")

    def ancho(self) -> int: return self._ancho
    def alto(self) -> int:  return self._alto

    def estaVacia(self) -> bool: return self._ancho == 0 or self._alto == 0

    def calcularEnergiaPixel(self, fila: int, col: int) -> float:
        def pixel(f: int, c: int) -> list:
            f = max(0, min(self._alto - 1, f))
            c = max(0, min(self._ancho - 1, c))
            return self._pixeles[f][c]

        energia = 0.0
        for canal in range(3):
            dx = float(pixel(fila, col + 1)[canal]) - float(pixel(fila, col - 1)[canal])
            dy = float(pixel(fila + 1, col)[canal]) - float(pixel(fila - 1, col)[canal])
            energia += dx * dx + dy * dy
        return math.sqrt(energia)

    def obtenerMatrizEnergia(self) -> list[list[float]]:
        energia = [[0.0] * self._ancho for _ in range(self._alto)]
        for f in range(self._alto):
            for c in range(self._ancho):
                energia[f][c] = self.calcularEnergiaPixel(f, c)
        return energia

    def eliminarSeam(self, seam: list[int]) -> None:
        if len(seam) != self._alto:
            raise RuntimeError("El seam debe tener exactamente una entrada por fila.")

        for f in range(self._alto):
            col = seam[f]
            self._pixeles[f].pop(col)
        self._ancho -= 1

from .figura import Figura
import math

class Hexagono(Figura):
    def desenhar(self, canvas):
        x_inicial, y_inicial, x_final, y_final = self.values
        centro_x = (x_inicial + x_final) / 2
        centro_y = (y_inicial + y_final) / 2
        raio_x = abs(x_final - x_inicial) / 2
        raio_y = abs(y_final - y_inicial) / 2
        raio = min(raio_x, raio_y)

        pontos = []
        for i in range(6):
            angulo = math.radians(-90 + i * 60)
            px = centro_x + raio * math.cos(angulo)
            py = centro_y + raio * math.sin(angulo)
            pontos.extend([px, py])

        return canvas.create_polygon(
            pontos,
            outline=self.cor_borda,
            fill=self.cor_preenchimento,
            width=self.espessura
        )

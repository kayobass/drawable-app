import math

from .figura import Figura


class TrianguloRetangulo(Figura):
    def desenhar(self, canvas):
        x_inicial, y_inicial, x_final, y_final = self.values

        return canvas.create_polygon(
            x_inicial, y_final,
            x_final, y_final,
            x_inicial, y_inicial,
            outline=self.cor_borda,
            fill=self.cor_preenchimento,
            width=self.espessura
        )


class TrianguloEquilatero(Figura):
    def desenhar(self, canvas):
        x_inicial, y_inicial, x_final, y_final = self.values

        lado = x_final - x_inicial
        altura_equilateral = lado * (3 ** 0.5) / 2
        y_final = y_inicial + altura_equilateral
        ponto_medio_x = (x_inicial + x_final) / 2

        return canvas.create_polygon(
            x_inicial, y_final,
            x_final, y_final,
            ponto_medio_x, y_inicial,
            outline=self.cor_borda,
            fill=self.cor_preenchimento,
            width=self.espessura
        )


class Pentagono(Figura):
    def desenhar(self, canvas):
        x_inicial, y_inicial, x_final, y_final = self.values
        centro_x = (x_inicial + x_final) / 2
        centro_y = (y_inicial + y_final) / 2
        raio_x = abs(x_final - x_inicial) / 2
        raio_y = abs(y_final - y_inicial) / 2
        raio = min(raio_x, raio_y)

        pontos = []
        for i in range(5):
            angulo = math.radians(-90 + i * 72)
            px = centro_x + raio * math.cos(angulo)
            py = centro_y + raio * math.sin(angulo)
            pontos.extend([px, py])

        return canvas.create_polygon(
            pontos,
            outline=self.cor_borda,
            fill=self.cor_preenchimento,
            width=self.espessura
        )


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


class Poligono(Figura):
    def adicionar_ponto(self, x, y):
        self.values.append((x, y))

    def desenhar_pontos_do_poligono(self, canvas):
        # Desenha as bolinhas nos vértices temporários
        for x, y in self.values:
            canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=self.cor_borda)

        if len(self.values) >= 2:
            for i in range(len(self.values) - 1):
                x_inicial, y_inicial = self.values[i]
                x_final, y_final = self.values[i + 1]
                canvas.create_line(x_inicial, y_inicial, x_final, y_final, fill=self.cor_borda, width=self.espessura,
                                   dash=(4, 2))

            # Liga o ponto atual de volta ao primeiro ponto com uma linha pontilhada guia
            x_prim, y_prim = self.values[0]
            x_ult, y_ult = self.values[-1]
            canvas.create_line(x_ult, y_ult, x_prim, y_prim, fill=self.cor_borda, width=self.espessura, dash=(2, 4))

    def desenhar(self, canvas):
        pontos = self.values

        if len(pontos) < 3:
            return None

        return canvas.create_polygon(
            pontos,
            outline=self.cor_borda,
            fill=self.cor_preenchimento,
            width=self.espessura
        )

from figura import Figura

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


from figura import Figura

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
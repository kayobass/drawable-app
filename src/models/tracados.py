from .figura import Figura

class Linha(Figura):
    def desenhar(self, canvas):
        x_inicial, y_inicial, x_final, y_final = self.values

        return canvas.create_line(
            x_inicial, y_inicial,
            x_final, y_final,
            fill=self.cor_borda,
            width=self.espessura
        )

class Rabisco(Figura):
    def desenhar(self, canvas):
        return canvas.create_line(
            self.values,
            fill=self.cor_borda,
            width=self.espessura
        )

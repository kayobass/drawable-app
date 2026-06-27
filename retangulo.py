from figura import Figura

class Retangulo(Figura):
    def desenhar(self, canvas):
        x_inicial, y_inicial, x_final, y_final = self.values
        canvas.create_rectangle(x_inicial, y_inicial, x_final, y_final, outline=self.cor_borda, fill=self.cor_preenchimento)
from figura import Figura


class Oval(Figura):
    def desenhar(self, canvas):
        x_inicial, y_inicial, x_final, y_final = self.values

        return canvas.create_oval(x_inicial, y_inicial, x_final, y_final, outline=self.cor_borda, fill=self.cor_preenchimento, width=self.espessura)
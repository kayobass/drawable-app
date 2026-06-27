from figura import Figura

class Rabisco(Figura):
    def desenhar(self, canvas):
        return canvas.create_line(self.values, fill=self.cor_borda, width=self.espessura)
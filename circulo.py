from figura import Figura

class Circulo(Figura):
    # Utilizando a ideia de transformar o retangulo diretor em quadrado para desenhar um circulo
    def oval_em_circulo(self, values):
        a, b, c, d = values
        largura = c - a
        altura = d - b
        tamanho = min(abs(largura), abs(altura))
        if largura < 0:
            c = a - tamanho
        else:
            c = a + tamanho
        if altura < 0:
            d = b - tamanho
        else:
            d = b + tamanho
        return a, b, c, d
    
    def desenhar(self, canvas):
        x_inicial, y_inicial, x_final, y_final = self.oval_em_circulo(self.values)

        return canvas.create_oval(
            x_inicial, y_inicial, 
            x_final, y_final, 
            outline=self.cor_borda, 
            fill=self.cor_preenchimento, 
            width=self.espessura
        )
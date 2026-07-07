from .figura import Figura

class Circulo(Figura):
    # Utilizando a ideia de transformar o retangulo diretor em quadrado para desenhar um circulo
    def transformar_em_circulo(self, values):
        x_inicial, y_inicial, x_final, y_final = values
        largura = x_final - x_inicial
        altura = y_final - y_inicial
        tamanho = min(abs(largura), abs(altura))

        if largura < 0:
            x_final = x_inicial - tamanho
        else:
            x_final = x_inicial + tamanho
        if altura < 0:
            y_final = y_inicial - tamanho
        else:
            y_final = y_inicial + tamanho

        return (
            x_inicial,
            y_inicial,
            x_final,
            y_final
        )

    def desenhar(self, canvas):
        x_inicial, y_inicial, x_final, y_final = self.transformar_em_circulo(self.values)

        return canvas.create_oval(
            x_inicial, y_inicial,
            x_final, y_final,
            outline=self.cor_borda,
            fill=self.cor_preenchimento,
            width=self.espessura
        )


class Oval(Figura):
    def desenhar(self, canvas):
        x_inicial, y_inicial, x_final, y_final = self.values

        return canvas.create_oval(
            x_inicial, y_inicial,
            x_final, y_final,
            outline=self.cor_borda,
            fill=self.cor_preenchimento,
            width=self.espessura
        )
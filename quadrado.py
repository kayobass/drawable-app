from figura import Figura

class Quadrado(Figura):
    def retangulo_em_quadrado(self, values):
        x_inicial, y_inicial, x_final, y_final = values
        largura = x_final - x_inicial
        altura = y_final - y_inicial

        lado  = min(abs(largura), abs(altura))

        if largura < 0:
            ladox = -lado
        else:
            ladox = lado
        if altura < 0:
            ladoy = -lado
        else:
            ladoy = lado
        return x_inicial, y_inicial, x_inicial + ladox, y_inicial + ladoy
    
    def desenhar(self, canvas):
        x_inicial, y_inicial, x_final, y_final = self.retangulo_em_quadrado(self.values)
        return canvas.create_rectangle(x_inicial, y_inicial, x_final, y_final, outline=self.cor_borda, fill=self.cor_preenchimento, width=self.espessura)
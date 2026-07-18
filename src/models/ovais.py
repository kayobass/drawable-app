"""
Módulo que contém as classes das figuras circulares e ovais.

Define o funcionamento do círculo e da oval, utilizando o canvas
para desenhar as figuras na interface.

:author: Matheuz Rozendo, Kayo Araujo
:version: OO.MVC.1
:since: OO.1
"""

from .figura import Figura


class Circulo(Figura):
    """
    Representa uma figura no formato de círculo.

    A classe ajusta as coordenadas recebidas para que a largura e a altura
    fiquem iguais. Depois disso, desenha o círculo no canvas.

    :author: Matheuz Rozendo, Kayo Araujo
    :version: OO.MVC.1
    :since: OO.1
    :see: Figura, Oval
    """

    def transformar_em_circulo(self, values):
        """
        Ajusta as coordenadas para formar um círculo.

        O método utiliza o menor valor entre a largura e a altura para
        deixar os dois lados com o mesmo tamanho.

        :param values: Coordenadas iniciais e finais usadas para formar o círculo.
        :return: Tupla com as coordenadas ajustadas do círculo.
        """
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

        return (x_inicial, y_inicial, x_final, y_final)

    def desenhar(self, canvas):
        """
        Desenha o círculo no canvas.

        Primeiro ajusta as coordenadas para formar um círculo e depois
        utiliza essas coordenadas para criar a figura.

        :param canvas: Área da interface onde o círculo será desenhado.
        :return: Identificador do círculo criado no canvas.
        :see: transformar_em_circulo
        """
        x_inicial, y_inicial, x_final, y_final = self.transformar_em_circulo(
            self.values
        )

        return canvas.create_oval(
            x_inicial,
            y_inicial,
            x_final,
            y_final,
            outline=self.cor_borda,
            fill=self.cor_preenchimento,
            width=self.espessura,
        )


class Oval(Figura):
    """
    Representa uma figura no formato oval.

    A classe utiliza as coordenadas, as cores e a espessura armazenadas
    para desenhar uma oval no canvas.

    :author: Matheuz Rozendo, Kayo Araujo
    :version: OO.MVC.1
    :since: OO.1
    :see: Figura, Circulo
    """

    def desenhar(self, canvas):
        """
        Desenha a oval no canvas.

        :param canvas: Área da interface onde a oval será desenhada.
        :return: Identificador da oval criada no canvas.
        """
        x_inicial, y_inicial, x_final, y_final = self.values

        return canvas.create_oval(
            x_inicial,
            y_inicial,
            x_final,
            y_final,
            outline=self.cor_borda,
            fill=self.cor_preenchimento,
            width=self.espessura,
        )

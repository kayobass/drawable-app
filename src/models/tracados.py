"""
Módulo que contém as classes responsáveis pelos traçados.

Define o funcionamento da linha reta e do rabisco livre,
utilizando o canvas para desenhar as figuras na interface.

:author: Matheuz Rozendo, Kayo Araujo
:version: OO.MVC.1
:since: OO.1
"""

from .figura import Figura


class Linha(Figura):
    """
    Representa uma linha reta formada por dois pontos.

    A classe utiliza as coordenadas inicial e final, a cor da borda
    e a espessura para desenhar a linha no canvas.

    :author: Matheuz Rozendo, Kayo Araujo
    :version: OO.MVC.1
    :since: OO.1
    :see: Figura, Rabisco
    """

    def desenhar(self, canvas):
        """ 
        Desenha uma linha reta no canvas. 

        :param canvas: Área da interface onde a linha será desenhada. 
        :return: Identificador da linha criada no canvas. 
        """
        x_inicial, y_inicial, x_final, y_final = self.values

        return canvas.create_line(
            x_inicial, y_inicial,
            x_final, y_final,
            fill=self.cor_borda,
            width=self.espessura
        )


class Rabisco(Figura):
    """
    Representa um rabisco desenhado livremente pelo usuário.

    A classe utiliza uma sequência de pontos para criar um traçado
    contínuo no canvas.

    :author: Matheuz Rozendo, Kayo Araujo
    :version: OO.MVC.1
    :since: OO.1
    :see: Figura, Linha
    """

    def desenhar(self, canvas):
        """ 
        Desenha o rabisco no canvas. 
        
        Os pontos armazenados na figura são ligados para formar
        um traçado contínuo.

        :param canvas: Área da interface onde o rabisco será desenhado. 
        :return: Identificador do rabisco criado no canvas. 
        """
        return canvas.create_line(
            self.values,
            fill=self.cor_borda,
            width=self.espessura
        )

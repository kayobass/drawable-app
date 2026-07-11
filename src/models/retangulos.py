"""
Módulo que contém as classes das figuras retangulares.

Define o funcionamento do retângulo e do quadrado, utilizando
o canvas para desenhar as figuras na interface.

@author: Matheuz Rozendo, Kayo Araujo
@version: OO.persiste.1
@since: OO.1
"""

from .figura import Figura


class Retangulo(Figura):
    """
    Representa uma figura no formato de retângulo.

    A classe utiliza as coordenadas, as cores e a espessura armazenadas
    para desenhar um retângulo no canvas.

    @author: Matheuz Rozendo, Kayo Araujo
    @version: OO.persiste.1
    @since: OO.1
    @see: Figura, Quadrado
    """

    def desenhar(self, canvas):
        """ 
        Desenha o retângulo no canvas.

        @param canvas: Área da interface onde o retângulo será desenhado. 
        @return: Identificador do retângulo criado no canvas. 
        """
        x_inicial, y_inicial, x_final, y_final = self.values

        return canvas.create_rectangle(
            x_inicial, y_inicial,
            x_final, y_final,
            outline=self.cor_borda,
            fill=self.cor_preenchimento,
            width=self.espessura
        )


class Quadrado(Figura):
    """
    Representa uma figura no formato de quadrado.

    A classe ajusta as coordenadas recebidas para que a largura e a altura
    tenham o mesmo tamanho. Depois disso, desenha o quadrado no canvas.

    @author: Matheuz Rozendo, Kayo Araujo
    @version: OO.persiste.1
    @since: OO.1
    @see: Figura, Retangulo
    """

    def retangulo_em_quadrado(self, values):
        """ 
        Ajusta as coordenadas de um retângulo para formar um quadrado. 

        O método utiliza o menor valor entre a largura e a altura para 
        definir o tamanho dos lados do quadrado. 

        @param values: Coordenadas iniciais e finais usadas para formar o quadrado.
        @return: Tupla com as coordenadas ajustadas do quadrado. 
        """
        x_inicial, y_inicial, x_final, y_final = values
        largura = x_final - x_inicial
        altura = y_final - y_inicial

        lado = min(abs(largura), abs(altura))

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
        """ 
        Desenha o quadrado no canvas. 

        Primeiro ajusta as coordenadas para formar um quadrado e depois 
        utiliza essas coordenadas para criar a figura.

        @param canvas: Área da interface onde o quadrado será desenhado. 
        @return: Identificador do quadrado criado no canvas. 
        @see: retangulo_em_quadrado 
        """
        x_inicial, y_inicial, x_final, y_final = self.retangulo_em_quadrado(self.values)

        return canvas.create_rectangle(
            x_inicial, y_inicial,
            x_final, y_final,
            outline=self.cor_borda,
            fill=self.cor_preenchimento,
            width=self.espessura
        )

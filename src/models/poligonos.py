"""
Módulo que contém as classes das figuras formadas por polígonos.

Define o funcionamento dos triângulos, pentágono, hexágono e do
polígono criado livremente pelo usuário.

@author: Matheuz Rozendo, Kayo Araujo
@version: OO.persiste.1
@since: OO.1
"""

import math

from .figura import Figura


class TrianguloRetangulo(Figura):
    """
    Representa uma figura no formato de triângulo retângulo.

    A classe utiliza as coordenadas guardadas na figura para definir
    os três pontos do triângulo e desenhá-lo no canvas.

    @author: Matheuz Rozendo, Kayo Araujo
    @version: OO.persiste.1
    @since: OO.1
    @see: Figura
    """

    def desenhar(self, canvas):
        """ 
        Desenha o triângulo retângulo no canvas. 

        @param canvas: Área da interface onde o triângulo será desenhado. 
        @return: Identificador do triângulo criado no canvas. 
        """
        x_inicial, y_inicial, x_final, y_final = self.values

        return canvas.create_polygon(
            x_inicial, y_final,
            x_final, y_final,
            x_inicial, y_inicial,
            outline=self.cor_borda,
            fill=self.cor_preenchimento,
            width=self.espessura
        )


class TrianguloEquilatero(Figura):
    """
    Representa uma figura no formato de triângulo equilátero.

    A classe calcula a altura e o ponto médio do triângulo a partir
    das coordenadas informadas pelo usuário.

    @author: Matheuz Rozendo, Kayo Araujo
    @version: OO.persiste.1
    @since: OO.1
    @see: Figura
    """

    def desenhar(self, canvas):
        """ 
        Calcula os pontos e desenha o triângulo equilátero no canvas. 

        @param canvas: Área da interface onde o triângulo será desenhado. 
        @return: Identificador do triângulo criado no canvas. 
        """
        x_inicial, y_inicial, x_final, y_final = self.values

        lado = x_final - x_inicial
        altura_equilateral = lado * (3 ** 0.5) / 2
        y_final = y_inicial + altura_equilateral
        ponto_medio_x = (x_inicial + x_final) / 2

        return canvas.create_polygon(
            x_inicial, y_final,
            x_final, y_final,
            ponto_medio_x, y_inicial,
            outline=self.cor_borda,
            fill=self.cor_preenchimento,
            width=self.espessura
        )


class Pentagono(Figura):
    """
    Representa uma figura no formato de pentágono.

    A classe calcula o centro, o raio e os cinco pontos necessários
    para desenhar o pentágono.

    @author: Matheuz Rozendo, Kayo Araujo
    @version: OO.persiste.1
    @since: OO.1
    @see: Figura
    """

    def desenhar(self, canvas):
        """ 
        Calcula os cinco pontos e desenha o pentágono no canvas. 

        @param canvas: Área da interface onde o pentágono será desenhado. 
        @return: Identificador do pentágono criado no canvas. 
        """
        x_inicial, y_inicial, x_final, y_final = self.values
        centro_x = (x_inicial + x_final) / 2
        centro_y = (y_inicial + y_final) / 2
        raio_x = abs(x_final - x_inicial) / 2
        raio_y = abs(y_final - y_inicial) / 2
        raio = min(raio_x, raio_y)

        pontos = []
        for i in range(5):
            angulo = math.radians(-90 + i * 72)
            px = centro_x + raio * math.cos(angulo)
            py = centro_y + raio * math.sin(angulo)
            pontos.extend([px, py])

        return canvas.create_polygon(
            pontos,
            outline=self.cor_borda,
            fill=self.cor_preenchimento,
            width=self.espessura
        )


class Hexagono(Figura):
    """
    Representa uma figura no formato de hexágono.

    A classe calcula o centro, o raio e os seis pontos necessários
    para desenhar o hexágono.

    @author: Matheuz Rozendo, Kayo Araujo
    @version: OO.persiste.1
    @since: OO.1
    @see: Figura
    """

    def desenhar(self, canvas):
        """ 
        Calcula os seis pontos e desenha o hexágono no canvas. 

        @param canvas: Área da interface onde o hexágono será desenhado. 
        @return: Identificador do hexágono criado no canvas. 
        """
        x_inicial, y_inicial, x_final, y_final = self.values
        centro_x = (x_inicial + x_final) / 2
        centro_y = (y_inicial + y_final) / 2
        raio_x = abs(x_final - x_inicial) / 2
        raio_y = abs(y_final - y_inicial) / 2
        raio = min(raio_x, raio_y)

        pontos = []
        for i in range(6):
            angulo = math.radians(-90 + i * 60)
            px = centro_x + raio * math.cos(angulo)
            py = centro_y + raio * math.sin(angulo)
            pontos.extend([px, py])

        return canvas.create_polygon(
            pontos,
            outline=self.cor_borda,
            fill=self.cor_preenchimento,
            width=self.espessura
        )


class Poligono(Figura):
    """
    Representa um polígono criado a partir dos pontos escolhidos pelo usuário.

    A classe permite adicionar pontos, mostrar um esboço durante a criação
    e desenhar o polígono final no canvas.

    @author: Matheuz Rozendo, Kayo Araujo
    @version: OO.persiste.1
    @since: OO.1
    @see: Figura
    """

    def adicionar_ponto(self, x, y):
        """ 
        Adiciona um novo ponto ao polígono.

        @param x: Coordenada do ponto no eixo X. 
        @param y: Coordenada do ponto no eixo Y. 
        @return: None 
        """
        self.values.append((x, y))

    def desenhar_pontos_do_poligono(self, canvas):
        """ 
        Desenha os pontos e as linhas temporárias do polígono. 

        Os pontos são mostrados como pequenos círculos e ligados por 
        linhas tracejadas enquanto o polígono ainda está sendo criado. 

        @param canvas: Área da interface onde o esboço será desenhado. 
        @return: None 
        """
        for x, y in self.values:
            canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=self.cor_borda)

        if len(self.values) >= 2:
            for i in range(len(self.values) - 1):
                x_inicial, y_inicial = self.values[i]
                x_final, y_final = self.values[i + 1]
                canvas.create_line(x_inicial, y_inicial, x_final, y_final, fill=self.cor_borda, width=self.espessura,
                                   dash=(4, 2))

            # Liga o ponto atual de volta ao primeiro ponto com uma linha pontilhada guia
            x_prim, y_prim = self.values[0]
            x_ult, y_ult = self.values[-1]
            canvas.create_line(x_ult, y_ult, x_prim, y_prim, fill=self.cor_borda, width=self.espessura, dash=(2, 4))

    def desenhar(self, canvas):
        """ 
        Desenha o polígono final no canvas. 

        O polígono só é desenhado quando possui pelo menos três pontos. 

        @param canvas: Área da interface onde o polígono será desenhado. 
        @return: Identificador do polígono criado no canvas ou None 
                 quando existem menos de três pontos. 
        """
        pontos = self.values

        if len(pontos) < 3:
            return None

        return canvas.create_polygon(
            pontos,
            outline=self.cor_borda,
            fill=self.cor_preenchimento,
            width=self.espessura
        )

"""
Módulo que contém a classe base das figuras do sistema.

Define os dados e os métodos que serão usados pelas diferentes
figuras do programa.

:author: Matheuz Rozendo, Kayo Araujo
:version: OO.persiste.1
:since: OO.1
"""

from abc import ABC, abstractmethod


class Figura(ABC):
    """
    Representa a classe base das figuras do sistema de desenho.

    A classe guarda os dados que todas as figuras possuem, como as coordenadas,
    a cor da borda, a cor do preenchimento e a espessura. Por ser uma classe
    abstrata, ela deve ser usada como base para as classes das figuras.

    :author: Matheuz Rozendo, Kayo Araujo
    :version: OO.persiste.1
    :since: OO.1
    :see: Retangulo, Oval, Poligono, Linha, Rabisco
    """

    def __init__(self, values, cor_borda, cor_preenchimento, espessura):
        """
        Inicializa os dados básicos de uma figura.

        :param values: Coordenadas ou pontos usados para formar a figura.
        :param cor_borda: Cor da borda da figura.
        :param cor_preenchimento: Cor do preenchimento da figura.
        :param espessura: Espessura da borda ou da linha da figura.
        :return: None
        """
        self.values = values
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
        self.espessura = espessura

    def __str__(self):
        """
        Retorna os dados da figura em formato de texto.

        O texto mostra o nome da classe da figura e os valores
        armazenados em seus atributos.

        :return: Texto com o nome e os dados da figura.
        """
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"

    def __eq__(self, other):
        """
        Compara a figura atual com outra figura.

        As figuras são consideradas iguais quando são do mesmo tipo
        e possuem as mesmas coordenadas, cores e espessura.

        :param other: Outra figura que será comparada com a figura atual.
        :return: True se as figuras forem iguais; False caso contrário.
        """
        if type(self) is not type(other):
            return False
        return (
            self.values == other.values
            and self.cor_borda == other.cor_borda
            and self.cor_preenchimento == other.cor_preenchimento
            and self.espessura == other.espessura
        )

    @abstractmethod
    def desenhar(self, canvas):
        """
        Define o método usado para desenhar uma figura no canvas.

        Cada classe filha deve implementar esse método de acordo
        com o tipo de figura que representa.

        :param canvas: Área da interface onde a figura será desenhada.
        :return: Identificador da figura criada no canvas, quando aplicável.
        """
        pass

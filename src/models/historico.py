"""
Módulo responsável pelo histórico das figuras do desenho.

Contém a classe que guarda as figuras adicionadas e controla
as ações de desfazer e refazer.

@author: Matheuz Rozendo, Kayo Araujo
@version: OO.persiste.1
@since: OO.MVC.1
"""

class Historico:
    """
    Controla o histórico de figuras do sistema de desenho.

    A classe guarda as figuras adicionadas e também as figuras que foram
    desfeitas. Com isso, permite realizar as ações de desfazer, refazer
    e limpar o desenho.

    @author: Matheuz Rozendo, Kayo Araujo
    @version: OO.persiste.1
    @since: OO.MVC.1
    """

    def __init__(self):
        """ 
        Inicializa o histórico do desenho. 

        Cria uma lista para guardar as figuras adicionadas e outra 
        para guardar as figuras que foram desfeitas. 

        @return: None 
        """
        self._figuras = []
        self._figuras_desfeitas = []

    @property
    def figuras(self):
        """ 
        Retorna as figuras que estão atualmente no desenho. 

        @return: Lista com as figuras adicionadas ao desenho. 
        """
        return self._figuras

    @property
    def figuras_desfeitas(self):
        """ 
        Retorna as figuras que foram desfeitas. 

        @return: Lista com as figuras disponíveis para serem refeitas. 
        """
        return self._figuras_desfeitas

    def adicionar(self, figura):
        """ 
        Adiciona uma nova figura ao histórico. 

        Quando uma nova figura é adicionada, a lista de figuras desfeitas
        é limpa, pois não será mais possível refazer as ações anteriores. 

        @param figura: Figura que será adicionada ao desenho. 
        @return: None 
        """
        self._figuras.append(figura)
        self._figuras_desfeitas.clear()

    def desfazer(self):
        """ 
        Desfaz a última figura adicionada ao desenho.

        A figura é retirada da lista principal e colocada na lista
        de figuras desfeitas.

        @return: None 
        @see: refazer 
        """
        if self._figuras:
            figura = self._figuras.pop()
            self._figuras_desfeitas.append(figura)

    def refazer(self):
        """ 
        Refaz a última figura que foi desfeita. 

        A figura é retirada da lista de figuras desfeitas e colocada 
        novamente na lista principal. 

        @return: None 
        @see: desfazer 
        """
        if self._figuras_desfeitas:
            figura = self._figuras_desfeitas.pop()
            self._figuras.append(figura)

    def limpar(self):
        """
        Limpa todo o histórico do desenho. 

        Remove as figuras adicionadas e também as figuras que foram desfeitas. 

        @return: None 
        """
        self._figuras.clear()
        self._figuras_desfeitas.clear()

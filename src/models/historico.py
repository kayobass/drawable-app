"""
Módulo responsável pelo histórico das figuras do desenho.

Contém a classe que guarda as figuras adicionadas e controla
as ações de desfazer e refazer.

:author: Matheuz Rozendo, Kayo Araujo
:version: OO.State.1
:since: OO.MVC.1
"""

import copy


class Historico:
    """
    Controla o histórico de figuras do sistema de desenho.

    Utiliza uma pilha unificada de ações para garantir que o desfazer/refazer
    respeite a ordem cronológica, independente do tipo de alteração
    (atributo, posição, reordenação ou criação/exclusão de figuras).

    :author: Matheuz Rozendo, Kayo Araujo
    :version: OO.State.1
    :since: OO.MVC.1
    """

    def __init__(self):
        """
        Inicializa o histórico do desenho.

        :return: None
        """
        self._figuras = []
        self._acoes = []
        self._acoes_refeitas = []

    @property
    def figuras(self):
        """
        Retorna as figuras que estão atualmente no desenho.

        :return: Lista com as figuras adicionadas ao desenho.
        """
        return self._figuras

    @property
    def figuras_desfeitas(self):
        """
        Retorna as figuras que foram desfeitas.

        Compatibility property — in the unified-stack system this is no longer
        the primary way to check redo state. Kept so external code that still
        references it does not break.

        :return: Lista vazia (redo state is tracked internally).
        """
        return []

    def adicionar(self, figura):
        """
        Adiciona uma nova figura ao histórico.

        :param figura: Figura que será adicionada ao desenho.
        :return: None
        """
        index = len(self._figuras)
        self._figuras.append(figura)
        self._acoes.append(("adicionar", index, figura))
        self._acoes_refeitas.clear()

    def inserir(self, indice, figura):
        """
        Insere uma figura em uma posição específica do histórico.

        :param indice: Posição onde a figura será inserida.
        :param figura: Figura que será inserida.
        :return: None
        """
        self._figuras.insert(indice, figura)
        self._acoes_refeitas.clear()

    def remover(self, figura):
        """
        Remove uma figura e registra a ação para desfazer.

        :param figura: Figura que será removida.
        :return: None
        """
        if figura in self._figuras:
            index = self._figuras.index(figura)
            self._figuras.pop(index)
            self._acoes.append(("remocao", index, figura))
            self._acoes_refeitas.clear()

    def registrar_mudanca_atributo(self, figura, atributo, valor_anterior, valor_novo):
        """
        Registra uma mudança de atributo de uma figura.

        :param figura: Figura que teve o atributo alterado.
        :param atributo: Nome do atributo alterado (ex: 'cor_borda').
        :param valor_anterior: Valor do atributo antes da mudança.
        :param valor_novo: Valor do atributo após a mudança.
        :return: None
        """
        self._acoes.append(("atributo", figura, atributo, valor_anterior, valor_novo))
        self._acoes_refeitas.clear()

    def registrar_posicao(self, figura, valores_anteriores):
        """
        Registra uma mudança de posição (coordenadas) de uma figura.

        :param figura: Figura que teve as coordenadas alteradas.
        :param valores_anteriores: Valores das coordenadas antes da movimentação.
        :return: None
        """
        valores_novos = copy.deepcopy(figura.values)
        self._acoes.append(
            ("posicao", figura, copy.deepcopy(valores_anteriores), valores_novos)
        )
        self._acoes_refeitas.clear()

    def registrar_movimentacao(self, ordem_anterior):
        """
        Registra uma mudança de ordem (z-order) das figuras.

        :param ordem_anterior: Lista com a ordem das figuras antes da movimentação.
        :return: None
        """
        self._acoes.append(("movimentacao", list(ordem_anterior), list(self._figuras)))
        self._acoes_refeitas.clear()

    def desfazer(self):
        """
        Desfaz a última ação registrada (LIFO).

        :return: Tipo da ação desfeita ou None se não houver nada para desfazer.
        """
        if not self._acoes:
            return None

        acao = self._acoes.pop()
        tipo = acao[0]

        if tipo == "remocao":
            _, index, figura = acao
            self._figuras.insert(index, figura)
        elif tipo == "adicionar":
            _, index, figura = acao
            self._figuras.pop(index)
        elif tipo == "atributo":
            _, figura, atributo, valor_anterior, valor_novo = acao
            setattr(figura, atributo, valor_anterior)
        elif tipo == "posicao":
            _, figura, valores_anteriores, valores_novos = acao
            figura.values = valores_anteriores
        elif tipo == "movimentacao":
            _, ordem_anterior, ordem_nova = acao
            self._figuras.clear()
            self._figuras.extend(ordem_anterior)

        self._acoes_refeitas.append(acao)
        return tipo

    def refazer(self):
        """
        Refaz a última ação desfeita (LIFO).

        :return: Tipo da ação refeita ou None se não houver nada para refazer.
        """
        if not self._acoes_refeitas:
            return None

        acao = self._acoes_refeitas.pop()
        tipo = acao[0]

        if tipo == "remocao":
            _, index, figura = acao
            self._figuras.pop(index)
        elif tipo == "adicionar":
            _, index, figura = acao
            self._figuras.insert(index, figura)
        elif tipo == "atributo":
            _, figura, atributo, valor_anterior, valor_novo = acao
            setattr(figura, atributo, valor_novo)
        elif tipo == "posicao":
            _, figura, valores_anteriores, valores_novos = acao
            figura.values = valores_novos
        elif tipo == "movimentacao":
            _, ordem_anterior, ordem_nova = acao
            self._figuras.clear()
            self._figuras.extend(ordem_nova)

        self._acoes.append(acao)
        return tipo

    def limpar(self):
        """
        Limpa todo o histórico do desenho.

        :return: None
        """
        self._figuras.clear()
        self._acoes.clear()
        self._acoes_refeitas.clear()

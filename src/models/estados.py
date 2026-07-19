"""
Módulo que contém as classes de estado do padrão State.

Define os estados possíveis da ferramenta de desenho, encapsulando
o comportamento que varia de acordo com a ferramenta selecionada.

:author: Matheuz Rozendo, Kayo Araujo
:version: OO.State.1
:since: OO.State.1
"""

from abc import ABC, abstractmethod


class EstadoFerramenta(ABC):
    """
    Classe base abstrata que define a interface dos estados da ferramenta.

    Cada estado concreto implementa o comportamento específico para
    um tipo de ferramenta, eliminando condicionais no controlador.

    :author: Kayo Araujo
    :since: OO.State.1
    """

    @abstractmethod
    def configurar_estado(self, controller):
        """
        Configura a interface de acordo com a ferramenta selecionada.

        :param controller: Controlador principal da aplicação.
        :return: None
        """
        pass

    @abstractmethod
    def iniciar_figura(self, controller, event):
        """
        Inicia a criação de uma figura ao pressionar o botão do mouse.

        :param controller: Controlador principal da aplicação.
        :param event: Evento do mouse com as coordenadas do clique.
        :return: None
        """
        pass

    @abstractmethod
    def atualizar_figura(self, controller, event):
        """
        Atualiza a figura enquanto o usuário arrasta o mouse.

        :param controller: Controlador principal da aplicação.
        :param event: Evento do mouse com a posição atual do cursor.
        :return: None
        """
        pass

    @abstractmethod
    def incluir_figura(self, controller, event):
        """
        Finaliza e inclui a figura no histórico ao soltar o botão do mouse.

        :param controller: Controlador principal da aplicação.
        :param event: Evento gerado ao soltar o botão do mouse.
        :return: None
        """
        pass

    @abstractmethod
    def desfazer(self, controller):
        """
        Realiza a ação de desfazer de acordo com o estado atual.

        :param controller: Controlador principal da aplicação.
        :return: None
        """
        pass

    @abstractmethod
    def refazer(self, controller):
        """
        Realiza a ação de refazer de acordo com o estado atual.

        :param controller: Controlador principal da aplicação.
        :return: None
        """
        pass


class EstadoLinha(EstadoFerramenta):
    """
    Estado da ferramenta Linha.

    Configura a interface para desenho de linhas retas,
    desabilitando os controles de preenchimento.

    :author: Kayo Araujo
    :since: OO.State.1
    """

    def configurar_estado(self, controller):
        controller.view.label_lados.grid_forget()
        controller.view.combo_lados.grid_forget()
        controller.view.botao_cor_preenchimento.config(state="disabled")
        controller.view.botao_sem_preenchimento.config(state="disabled")
        controller.view.indicador_preenchimento.config(bg="#D3D3D3")
        controller.view.botao_cor_borda.config(text="Cor")

    def iniciar_figura(self, controller, event):
        controller.figura_nova = controller.MAPA_FIGURAS[controller.ferramenta](
            [event.x, event.y, event.x, event.y],
            controller.cor_da_borda,
            controller.cor_do_preenchimento,
            controller.espessura,
        )

    def atualizar_figura(self, controller, event):
        if controller.figura_nova:
            controller.figura_nova.values[2] = event.x
            controller.figura_nova.values[3] = event.y
            controller.desenhar_figuras()
            controller.desenhar_figura_nova()

    def incluir_figura(self, controller, event):
        if controller.figura_nova and not controller.incompleta(controller.figura_nova):
            controller.historico.adicionar(controller.figura_nova)
        controller.figura_nova = None
        controller.verifica_historico()
        controller.desenhar_figuras()

    def desfazer(self, controller):
        if controller.historico.figuras:
            controller.historico.desfazer()
            controller.verifica_historico()
            controller.desenhar_figuras()

    def refazer(self, controller):
        if controller.historico.figuras_desfeitas:
            controller.historico.refazer()
            controller.verifica_historico()
            controller.desenhar_figuras()


class EstadoRabisco(EstadoFerramenta):
    """
    Estado da ferramenta Rabisco.

    Configura a interface para desenho livre,
    desabilitando os controles de preenchimento.

    :author: Kayo Araujo
    :since: OO.State.1
    """

    def configurar_estado(self, controller):
        controller.view.label_lados.grid_forget()
        controller.view.combo_lados.grid_forget()
        controller.view.botao_cor_preenchimento.config(state="disabled")
        controller.view.botao_sem_preenchimento.config(state="disabled")
        controller.view.indicador_preenchimento.config(bg="#D3D3D3")
        controller.view.botao_cor_borda.config(text="Cor")

    def iniciar_figura(self, controller, event):
        controller.figura_nova = controller.MAPA_FIGURAS[controller.ferramenta](
            [(event.x, event.y)],
            controller.cor_da_borda,
            controller.cor_do_preenchimento,
            controller.espessura,
        )

    def atualizar_figura(self, controller, event):
        if controller.figura_nova:
            controller.figura_nova.values.append((event.x, event.y))
            controller.desenhar_figuras()
            controller.desenhar_figura_nova()

    def incluir_figura(self, controller, event):
        if controller.figura_nova and not controller.incompleta(controller.figura_nova):
            controller.historico.adicionar(controller.figura_nova)
        controller.figura_nova = None
        controller.verifica_historico()
        controller.desenhar_figuras()

    def desfazer(self, controller):
        if controller.historico.figuras:
            controller.historico.desfazer()
            controller.verifica_historico()
            controller.desenhar_figuras()

    def refazer(self, controller):
        if controller.historico.figuras_desfeitas:
            controller.historico.refazer()
            controller.verifica_historico()
            controller.desenhar_figuras()


class EstadoFigura(EstadoFerramenta):
    """
    Estado para figuras com preenchimento (Oval, Círculo, Retângulo, etc).

    Configura a interface habilitando os controles de preenchimento.

    :author: Kayo Araujo
    :since: OO.State.1
    """

    def configurar_estado(self, controller):
        controller.view.label_lados.grid_forget()
        controller.view.combo_lados.grid_forget()
        controller.view.botao_cor_preenchimento.config(state="normal")
        controller.view.botao_sem_preenchimento.config(state="normal")
        controller.view.indicador_preenchimento.config(
            bg=controller.cor_do_preenchimento or "#D3D3D3"
        )
        controller.view.botao_cor_borda.config(text="Cor da borda")

    def iniciar_figura(self, controller, event):
        controller.figura_nova = controller.MAPA_FIGURAS[controller.ferramenta](
            [event.x, event.y, event.x, event.y],
            controller.cor_da_borda,
            controller.cor_do_preenchimento,
            controller.espessura,
        )

    def atualizar_figura(self, controller, event):
        if controller.figura_nova:
            controller.figura_nova.values[2] = event.x
            controller.figura_nova.values[3] = event.y
            controller.desenhar_figuras()
            controller.desenhar_figura_nova()

    def incluir_figura(self, controller, event):
        if controller.figura_nova and not controller.incompleta(controller.figura_nova):
            controller.historico.adicionar(controller.figura_nova)
        controller.figura_nova = None
        controller.verifica_historico()
        controller.desenhar_figuras()

    def desfazer(self, controller):
        if controller.historico.figuras:
            controller.historico.desfazer()
            controller.verifica_historico()
            controller.desenhar_figuras()

    def refazer(self, controller):
        if controller.historico.figuras_desfeitas:
            controller.historico.refazer()
            controller.verifica_historico()
            controller.desenhar_figuras()


class EstadoPoligono(EstadoFerramenta):
    """
    Estado da ferramenta Polígono.

    Configura a interface para criação interativa de polígonos,
    exibindo o seletor de quantidade de lados.

    :author: Kayo Araujo
    :since: OO.State.1
    """

    def configurar_estado(self, controller):
        controller.view.label_lados.grid(row=0, column=2, sticky="w")
        controller.view.combo_lados.grid(row=0, column=3, sticky="w")
        controller.view.botao_cor_preenchimento.config(state="normal")
        controller.view.botao_sem_preenchimento.config(state="normal")
        controller.view.indicador_preenchimento.config(
            bg=controller.cor_do_preenchimento or "#D3D3D3"
        )
        controller.view.botao_cor_borda.config(text="Cor da borda")

        if controller.poligono_atual is not None:
            controller.poligono_atual = None
            controller.desenhar_figuras()

    def iniciar_figura(self, controller, event):
        if controller.poligono_atual is None:
            controller.poligono_atual = controller.MAPA_FIGURAS[controller.ferramenta](
                [],
                controller.cor_da_borda,
                controller.cor_do_preenchimento,
                controller.espessura,
            )

        controller.poligono_atual.adicionar_ponto(event.x, event.y)
        controller.desenhar_figuras()
        controller.poligono_atual.desenhar_pontos_do_poligono(controller.view.canvas)

        if (
            len(controller.poligono_atual.values)
            == controller.view.lados_poligono.get()
        ):
            controller.estado.finalizar(controller)

    def atualizar_figura(self, controller, event):
        pass

    def incluir_figura(self, controller, event):
        pass

    def finalizar(self, controller):
        if (
            controller.poligono_atual is not None
            and len(controller.poligono_atual.values) >= 3
        ):
            controller.historico.adicionar(controller.poligono_atual)
        controller.poligono_atual = None
        controller.verifica_historico()
        controller.desenhar_figuras()

    def desfazer(self, controller):
        if controller.poligono_atual is not None:
            controller.poligono_atual = None
            controller.desenhar_figuras()
            return

        if controller.historico.figuras:
            controller.historico.desfazer()
            controller.verifica_historico()
            controller.desenhar_figuras()

    def refazer(self, controller):
        if controller.poligono_atual is not None:
            controller.poligono_atual = None
            controller.desenhar_figuras()
            return

        if controller.historico.figuras_desfeitas:
            controller.historico.refazer()
            controller.verifica_historico()
            controller.desenhar_figuras()


class EstadoSelecao(EstadoFerramenta):
    """
    Estado responsável pela seleção e movimentação das figuras.

    Permite selecionar uma figura ao clicar sobre ela e movê-la enquanto
    o botão esquerdo do mouse permanece pressionado.

    :author: Matheuz Rozendo
    :since: OO.State.1
    """

    def configurar_estado(self, controller):
        controller.view.label_lados.grid_forget()
        controller.view.combo_lados.grid_forget()

        controller.view.botao_cor_preenchimento.config(state="normal")
        controller.view.botao_sem_preenchimento.config(state="normal")
        controller.view.botao_cor_borda.config(text="Cor da borda")

        controller.figura_nova = None
        controller.poligono_atual = None

    def iniciar_figura(self, controller, event):
        """
        Seleciona uma figura e registra a posição inicial do mouse.

        :param controller: Controlador principal da aplicação.
        :param event: Evento do mouse com as coordenadas do clique.
        :return: None
        """
        import copy

        controller.selecionar_figura(event.x, event.y)
        if controller.figura_selecionada is not None:
            controller.ultima_posicao_mouse = (event.x, event.y)
            controller._posicao_inicial_arraste = copy.deepcopy(
                controller.figura_selecionada.values
            )
        else:
            controller.ultima_posicao_mouse = None
            controller._posicao_inicial_arraste = None

    def atualizar_figura(self, controller, event):
        """
        Move a figura selecionada durante o arraste do mouse.

        Calcula o deslocamento em relação à posição anterior do cursor
        e solicita ao controlador que atualize as coordenadas da figura.

        :param controller: Controlador principal da aplicação.
        :param event: Evento do mouse com a posição atual do cursor.
        :return: None
        """

        if (
            controller.figura_selecionada is None
            or controller.ultima_posicao_mouse is None
        ):
            return

        x_anterior, y_anterior = controller.ultima_posicao_mouse

        deslocamento_x = event.x - x_anterior
        deslocamento_y = event.y - y_anterior

        controller.mover_figura_selecionada(deslocamento_x, deslocamento_y)

        controller.ultima_posicao_mouse = (event.x, event.y)

    def incluir_figura(self, controller, event):
        """
        Finaliza a movimentação da figura selecionada.

        Se a figura foi movida, registra a mudança de posição no histórico.
        Remove o registro da última posição do mouse quando o botão
        esquerdo é solto.

        :param controller: Controlador principal da aplicação.
        :param event: Evento gerado ao soltar o botão do mouse.
        :return: None
        """
        if (
            controller.figura_selecionada is not None
            and controller._posicao_inicial_arraste is not None
        ):
            valores_atuais = controller.figura_selecionada.values
            valores_anteriores = controller._posicao_inicial_arraste
            if valores_atuais != valores_anteriores:
                controller.historico.registrar_posicao(
                    controller.figura_selecionada, valores_anteriores
                )
                controller._alterado = True

        controller.ultima_posicao_mouse = None
        controller._posicao_inicial_arraste = None

    def desfazer(self, controller):
        if controller.historico.figuras:
            controller.historico.desfazer()
            controller.verifica_historico()
            controller.desenhar_figuras()

    def refazer(self, controller):
        if controller.historico.figuras_desfeitas:
            controller.historico.refazer()
            controller.verifica_historico()
            controller.desenhar_figuras()


MAPA_ESTADOS = {
    "Selecionar": EstadoSelecao,
    "Linha": EstadoLinha,
    "Rabisco": EstadoRabisco,
    "Poligono": EstadoPoligono,
}

FERRAMENTAS_COM_PREENCHIMENTO = {
    "Oval",
    "Circulo",
    "Retangulo",
    "Quadrado",
    "Triangulo",
    "Triangulo Retangulo",
    "Pentagono",
    "Hexagono",
}


def obter_estado(ferramenta):
    """
    Retorna a instância do estado correspondente à ferramenta.

    :param ferramenta: Nome da ferramenta selecionada.
    :return: Instância de EstadoFerramenta.
    :see: MAPA_ESTADOS, FERRAMENTAS_COM_PREENCHIMENTO, EstadoFigura
    """
    classe_estado = MAPA_ESTADOS.get(ferramenta)
    if classe_estado:
        return classe_estado()
    if ferramenta in FERRAMENTAS_COM_PREENCHIMENTO:
        return EstadoFigura()
    return EstadoLinha()

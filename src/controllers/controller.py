"""
Módulo responsável pelo controle do sistema de desenho.

Contém o controlador principal da aplicação, responsável por conectar
a visão ao histórico e às classes de figuras, além de controlar eventos,
comandos, criação de desenhos, persistência e fechamento do sistema.

:author: Matheuz Rozendo, Kayo Araujo
:since: OO.State.1
"""

import pickle
from tkinter import colorchooser, messagebox, filedialog

from models.ovais import Circulo, Oval
from models.poligonos import (
    TrianguloEquilatero,
    TrianguloRetangulo,
    Pentagono,
    Hexagono,
    Poligono,
)
from models.retangulos import Retangulo, Quadrado
from models.tracados import Linha, Rabisco
from models.estados import obter_estado


class DrawableController:
    """
    Controla as ações e os eventos do sistema de desenho.

    A classe faz a ligação entre a interface, o histórico e as classes das figuras.
    Utiliza o padrão State para delegar o comportamento variável de cada ferramenta
    a objetos de estado, eliminando condicionais no controlador.

    :author: Matheuz Rozendo, Kayo Araujo
    :since: OO.State.1
    :see: DrawableView, Historico, EstadoFerramenta
    """

    MAPA_FIGURAS = {
        "Linha": Linha,
        "Rabisco": Rabisco,
        "Oval": Oval,
        "Circulo": Circulo,
        "Retangulo": Retangulo,
        "Triangulo": TrianguloEquilatero,
        "Triangulo Retangulo": TrianguloRetangulo,
        "Quadrado": Quadrado,
        "Pentagono": Pentagono,
        "Hexagono": Hexagono,
        "Poligono": Poligono,
    }

    def __init__(self, view, historico):
        """
        Inicializa o controlador do sistema de desenho.

        Guarda a visão e o histórico que serão usados pelo controlador.
        Também define os valores iniciais das cores e das figuras e configura
        os comandos e eventos da interface.

        :param view: visão usada para acessar e atualizar a interface gráfica.
        :param historico: Histórico usado para guardar as figuras e controlar
        as ações de desfazer e refazer.

        :return: None
        :see: configurar_comandos, configurar_eventos, atribuir_foco_canvas
        """
        self.view = view
        self.historico = historico

        self.cor_da_borda = "black"
        self.cor_do_preenchimento = ""

        self.figura_nova = None
        self.poligono_atual = None
        self.figura_selecionada = None
        self.itens_figuras = {}
        self.ultima_posicao_mouse = None
        self.arquivo_atual = None
        self.figuras_carregadas = []

        self.estado = obter_estado(self.ferramenta)
        self.estado.configurar_estado(self)

        self.configurar_comandos()
        self.configurar_eventos()
        self.atribuir_foco_canvas()

    @classmethod
    def figuras_disponiveis(cls):
        """
        Retorna os nomes das figuras disponíveis no sistema.

        Os nomes são obtidos a partir das chaves armazenadas em MAPA_FIGURAS.

        :return: Lista com os nomes das figuras disponíveis.
        :see: MAPA_FIGURAS
        """
        return ["Selecionar"] + list(cls.MAPA_FIGURAS.keys())

    @property
    def ferramenta(self):
        """
        Retorna a ferramenta selecionada atualmente na interface.

        :return: Nome da figura selecionada pelo usuário.
        """
        return self.view.tipo_figura.get()

    @property
    def espessura(self):
        """
        Retorna a espessura de linha selecionada na interface.

        :return: Valor da espessura selecionada pelo usuário.
        """
        return self.view.espessura.get()

    def configurar_comandos(self):
        """
        Associa os botões e controles da interface aos métodos do controlador.

        :return: None
        :see: salvar_desenho, carregar_desenho, detecta_mudanca
        """
        self.view.root.protocol("WM_DELETE_WINDOW", self.fechar_app)

        self.view.botao_salvar.config(command=self.salvar_desenho)
        self.view.botao_carregar.config(command=self.carregar_desenho)

        self.view.botao_cor_borda.config(command=self.escolher_cor_da_borda)
        self.view.botao_cor_preenchimento.config(
            command=self.escolher_cor_do_preenchimento
        )
        self.view.botao_sem_preenchimento.config(command=self.remover_preenchimento)

        self.view.tipo_figura.trace_add("write", self.detecta_mudanca)
        self.view.lados_poligono.trace_add("write", self.detecta_mudanca)
        self.view.espessura.trace_add("write", self.alterar_espessura)

        self.detecta_mudanca()

    def configurar_eventos(self):
        """
        Configura os eventos do mouse e os atalhos do teclado.

        :return: None
        """
        self.view.canvas.bind("<ButtonPress-1>", self.iniciar_figura_nova)
        self.view.canvas.bind("<B1-Motion>", self.atualizar_figura_nova)
        self.view.canvas.bind("<ButtonRelease-1>", self.incluir_figura_nova)
        self.view.canvas.bind("<Button-3>", self.finalizar_poligono)

        self.view.root.bind_all("<Escape>", self.cancelar_acao)
        self.view.root.bind_all("<Control-z>", self.desfazer)
        self.view.root.bind_all("<Control-y>", self.refazer)
        self.view.root.bind_all("<Delete>", self.excluir_figura_selecionada)
        self.view.root.bind_all("<Right>", self.mover_posicao_frente)
        self.view.root.bind_all("<Left>", self.mover_posicao_tras)
        self.view.root.bind_all("<Up>", self.mover_posicao_topo)
        self.view.root.bind_all("<Down>", self.mover_posicao_fundo)

        self.view.canvas.focus_set()

    def atribuir_foco_canvas(self):
        """
        Configura o retorno do foco ao canvas após alterações nos seletores.

        :return: None
        """
        self.view.combo_lados.bind(
            "<<ComboboxSelected>>", lambda event: self.view.canvas.focus_set()
        )

        self.view.combo_espessura.bind(
            "<<ComboboxSelected>>", lambda event: self.view.canvas.focus_set()
        )

    def escolher_cor_da_borda(self):
        """
        Abre o seletor de cores e altera a cor da borda.

        Se houver uma figura selecionada, altera também a cor dela.
        Caso contrário, a cor será usada nas próximas figuras.

        :return: None
        """
        cor = colorchooser.askcolor(title="Cor da borda")
        if cor[1] is not None:
            self.cor_da_borda = cor[1]
            self.view.indicador_borda.config(bg=self.cor_da_borda)
            if self.figura_selecionada is not None:
                self.figura_selecionada.cor_borda = self.cor_da_borda
                self.desenhar_figuras()

    def escolher_cor_do_preenchimento(self):
        """
        Abre o seletor de cores e altera a cor de preenchimento.

        Se houver uma figura selecionada, altera também o preenchimento dela.
        Caso contrário, a cor será usada nas próximas figuras.

        :return: None
        """
        corp = colorchooser.askcolor(title="Cor do preenchimento")
        if corp[1] is not None:
            self.cor_do_preenchimento = corp[1]
            self.view.indicador_preenchimento.config(bg=self.cor_do_preenchimento)
            if self.figura_selecionada is not None:
                self.figura_selecionada.cor_preenchimento = self.cor_do_preenchimento
                self.desenhar_figuras()

    def remover_preenchimento(self):
        """
        Remove a cor de preenchimento.
        Se houver uma figura selecionada, remove também o preenchimento dela.

        :return: None
        """
        self.cor_do_preenchimento = ""
        self.view.indicador_preenchimento.config(bg="#D3D3D3")
        if self.figura_selecionada is not None:
            self.figura_selecionada.cor_preenchimento = ""
            self.desenhar_figuras()

    def detecta_mudanca(self, *args):
        """
        Atualiza a interface e o estado quando a ferramenta ou a quantidade de lados muda.

        Delega a configuração da interface ao estado atual.

        :param args: Informações enviadas automaticamente pelo Tkinter.
        :return: None
        :see: obter_estado
        """
        self.estado = obter_estado(self.ferramenta)
        self.estado.configurar_estado(self)

    def alterar_espessura(self, *args):
        """
        Atualiza a espessura utilizada no desenho.

        Se houver uma figura selecionada, altera também a espessura dela.

        :param args: Informações enviadas automaticamente pelo Tkinter.
        :return: None
        """
        if self.figura_selecionada is not None:
            self.figura_selecionada.espessura = self.espessura
            self.desenhar_figuras()

        self.view.canvas.focus_set()

    def verifica_historico(self):
        """
        Atualiza o estado do botão de salvar conforme o conteúdo do histórico.

        :return: None
        """
        if self.historico.figuras:
            self.view.botao_salvar.config(state="normal")
        else:
            self.view.botao_salvar.config(state="disabled")

    def iniciar_figura_nova(self, event):
        """
        Inicia uma nova figura de acordo com a ferramenta selecionada.

        Delega a criação ao estado atual.

        :param event: Evento do mouse que contém as coordenadas do clique.
        :return: None
        """
        self.estado.iniciar_figura(self, event)

    def atualizar_figura_nova(self, event):
        """
        Atualiza a figura enquanto o usuário arrasta o mouse.

        Delega a atualização ao estado atual.

        :param event: Evento do mouse que contém a posição atual do cursor.
        :return: None
        """
        self.estado.atualizar_figura(self, event)

    def incluir_figura_nova(self, event):
        """
        Finaliza a figura atual e a adiciona ao histórico.

        Delega a finalização ao estado atual.

        :param event: Evento gerado quando o botão do mouse é solto.
        :return: None
        """
        self.estado.incluir_figura(self, event)

    def finalizar_poligono(self, event):
        """
        Finaliza o polígono que está sendo criado (via clique direito).

        Delega a finalização ao estado atual.

        :param event: Evento do mouse ou None quando a finalização ocorre automaticamente.
        :return: None
        """
        if hasattr(self.estado, "finalizar"):
            self.estado.finalizar(self)

    def desenhar_figuras(self):
        """
        Desenha novamente todas as figuras armazenadas no histórico.

        O método limpa o canvas, redesenha as figuras e associa cada
        identificador criado no canvas ao respectivo objeto de figura.
        Caso uma figura esteja selecionada, seu contorno é exibido
        de forma tracejada.

        :return: None
        :see: selecionar_figura
        """

        self.view.canvas.delete("all")
        self.itens_figuras.clear()
        for figura in self.historico.figuras:
            id_desenho = figura.desenhar(self.view.canvas)
            if id_desenho is not None:
                self.itens_figuras[id_desenho] = figura
                if figura is self.figura_selecionada:
                    self.view.canvas.itemconfig(id_desenho, dash=(4, 2))

    def selecionar_figura(self, x, y):
        """
        Seleciona a figura localizada na posição clicada.

        O método procura itens do canvas próximos às coordenadas recebidas.
        Quando existem figuras sobrepostas, seleciona a figura que estiver
        visualmente mais acima. Caso nenhuma figura seja encontrada, a
        seleção atual é removida.

        :param x: Coordenada horizontal do clique.
        :param y: Coordenada vertical do clique.
        :return: None
        :see: desenhar_figuras
        """

        margem = 4

        itens_encontrados = self.view.canvas.find_overlapping(
            x - margem, y - margem, x + margem, y + margem
        )

        self.figura_selecionada = None

        for id_item in reversed(itens_encontrados):
            if id_item in self.itens_figuras:
                self.figura_selecionada = self.itens_figuras[id_item]
                break

        self.atualizar_indicadores()
        self.desenhar_figuras()
        self.view.canvas.focus_set()

    def atualizar_indicadores(self):
        """
        Atualiza os indicadores da view com base na figura selecionada.

        Se houver uma figura selecionada, sincroniza as cores, espessura
        e preenchimento da interface com os valores da figura.

        :return: None
        """
        if self.figura_selecionada is None:
            return

        self.cor_da_borda = self.figura_selecionada.cor_borda
        self.cor_do_preenchimento = self.figura_selecionada.cor_preenchimento

        self.view.indicador_borda.config(bg=self.cor_da_borda)
        self.view.espessura.set(self.figura_selecionada.espessura)

        if isinstance(self.figura_selecionada, (Linha, Rabisco)):
            self.view.botao_cor_borda.config(text="Cor")
            self.view.botao_cor_preenchimento.config(state="disabled")
            self.view.botao_sem_preenchimento.config(state="disabled")
            self.view.indicador_preenchimento.config(bg="#D3D3D3")
        else:
            self.view.botao_cor_borda.config(text="Cor da borda")
            self.view.botao_cor_preenchimento.config(state="normal")
            self.view.botao_sem_preenchimento.config(state="normal")
            self.view.indicador_preenchimento.config(
                bg=self.cor_do_preenchimento if self.cor_do_preenchimento else "#D3D3D3"
            )

    def mover_figura_selecionada(self, deslocamento_x, deslocamento_y):
        """
        Move a figura selecionada pela quantidade informada.

        O método altera as coordenadas da figura com base nos deslocamentos
        horizontal e vertical recebidos. Figuras formadas por vários pontos,
        como polígonos e rabiscos, têm todos os seus pontos atualizados.

        :param deslocamento_x: Distância horizontal percorrida pelo mouse.
        :param deslocamento_y: Distância vertical percorrida pelo mouse.
        :return: None
        :see: selecionar_figura, desenhar_figuras
        """

        if self.figura_selecionada is None:
            return

        valores = self.figura_selecionada.values

        if not valores:
            return

        if isinstance(valores[0], (tuple, list)):
            self.figura_selecionada.values = [
                (x + deslocamento_x, y + deslocamento_y) for x, y in valores
            ]

        else:
            for indice in range(0, len(valores), 2):
                valores[indice] += deslocamento_x
                valores[indice + 1] += deslocamento_y

        self.desenhar_figuras()

    def desenhar_figura_nova(self):
        """
        Desenha temporariamente a figura que está sendo criada.

        A figura temporária recebe uma linha tracejada para mostrar que ainda
        não foi adicionada ao histórico.

        :return: None
        """
        if self.figura_nova:
            id_desenho = self.figura_nova.desenhar(self.view.canvas)
            if id_desenho:
                self.view.canvas.itemconfig(id_desenho, dash=(4, 2))

    def incompleta(self, figura):
        """
        Verifica se uma figura está incompleta.

        :param figura: Figura que será verificada.
        :return: True se a figura estiver incompleta e False caso contrário.
        """
        if isinstance(figura, Rabisco):
            return len(figura.values) <= 1
        return (figura.values[0], figura.values[1]) == (
            figura.values[2],
            figura.values[3],
        )

    def desfazer(self, *args):
        """
        Desfaz a última ação.

        Verifica primeiro se há movimentações para desfazer.
        Caso contrário, delega a ação ao estado atual.

        :param args: Argumentos opcionais enviados pelo evento de teclado.
        :return: None
        """
        if self.historico.desfazer_movimentacao():
            self.desenhar_figuras()
            return
        self.estado.desfazer(self)

    def refazer(self, *args):
        """
        Refaz a última ação desfeita.

        Verifica primeiro se há movimentações para refazer.
        Caso contrário, delega a ação ao estado atual.

        :param args: Argumentos opcionais enviados pelo evento de teclado.
        :return: None
        """
        if self.historico.refazer_movimentacao():
            self.desenhar_figuras()
            return
        self.estado.refazer(self)

    def excluir_figura_selecionada(self, event=None):
        """
        Remove a figura atualmente selecionada do canvas e do histórico.

        :param event: Evento opcional do teclado (ex: tecla Delete).
        :return: None
        """
        if self.figura_selecionada is not None:
            self.historico.desfazer(self.figura_selecionada)
            self.figura_selecionada = None
            self.desenhar_figuras()
            self.verifica_historico()

    def mover_posicao_frente(self, event=None):
        """
        Move a figura selecionada uma posição para frente na ordem de desenho.

        :param event: Evento opcional da tecla seta para a direita.
        :return: None
        """
        if self.figura_selecionada is None:
            return

        figuras = self.historico.figuras
        indice = figuras.index(self.figura_selecionada)

        if indice < len(figuras) - 1:
            ordem_anterior = list(figuras)
            figuras[indice], figuras[indice + 1] = figuras[indice + 1], figuras[indice]
            self.historico.registrar_movimentacao(ordem_anterior)
            self.desenhar_figuras()

    def mover_posicao_tras(self, event=None):
        """
        Move a figura selecionada uma posição para trás na ordem de desenho.

        :param event: Evento opcional da tecla seta para a esquerda.
        :return: None
        """
        if self.figura_selecionada is None:
            return

        figuras = self.historico.figuras
        indice = figuras.index(self.figura_selecionada)

        if indice > 0:
            ordem_anterior = list(figuras)
            figuras[indice], figuras[indice - 1] = figuras[indice - 1], figuras[indice]
            self.historico.registrar_movimentacao(ordem_anterior)
            self.desenhar_figuras()

    def mover_posicao_topo(self, event=None):
        """
        Move a figura selecionada para o topo da ordem de desenho (último lugar da lista).

        :param event: Evento opcional da tecla de atalho.
        :return: None
        """
        if self.figura_selecionada is None:
            return

        figuras = self.historico.figuras
        indice = figuras.index(self.figura_selecionada)

        if indice < len(figuras) - 1:
            ordem_anterior = list(figuras)
            figuras.append(figuras.pop(indice))
            self.historico.registrar_movimentacao(ordem_anterior)
            self.desenhar_figuras()

    def mover_posicao_fundo(self, event=None):
        """
        Move a figura selecionada para o fundo da ordem de desenho (primeira posição da lista).

        :param event: Evento opcional da tecla de atalho.
        :return: None
        """
        if self.figura_selecionada is None:
            return

        figuras = self.historico.figuras
        indice = figuras.index(self.figura_selecionada)

        if indice > 0:
            ordem_anterior = list(figuras)
            figuras.insert(0, figuras.pop(indice))
            self.historico.registrar_movimentacao(ordem_anterior)
            self.desenhar_figuras()

    def cancelar_acao(self, event=None):
        """
        Cancela a ação em andamento ao pressionar a tecla Esc.

        Desceleciona figuras, cancela polígonos em criação e
        cancela figuras sendo desenhadas.

        :param event: Evento da tecla Esc.
        :return: None
        """
        if self.figura_selecionada is not None:
            self.figura_selecionada = None
            self.desenhar_figuras()
            return

        if self.poligono_atual is not None:
            self.poligono_atual = None
            self.desenhar_figuras()
            return

        if self.figura_nova is not None:
            self.figura_nova = None
            self.desenhar_figuras()
            return

    def esta_alterado(self):
        """
        Verifica se o desenho atual possui alterações ainda não salvas.

        :return: True quando existem alterações não salvas; False caso contrário.
        """
        if not self.historico.figuras:
            return False

        return (
            self.historico.figuras != self.figuras_carregadas
            or self.arquivo_atual is None
        )

    def salvar_desenho(self):
        """
        Salva o desenho atual em um arquivo Pickle.

        :return: True se o desenho for salvo; None caso contrário.
        """
        if not self.historico.figuras:
            messagebox.showwarning("Aviso", "Não há nada para salvar!")
            return

        if self.arquivo_atual:
            caminho_para_salvar = self.arquivo_atual
        else:
            caminho_para_salvar = filedialog.asksaveasfilename(
                defaultextension=".pkl",
                filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")],
            )

        if caminho_para_salvar:
            try:
                with open(caminho_para_salvar, "wb") as f:
                    pickle.dump(self.historico.figuras, f)

                self.figuras_carregadas = self.historico.figuras.copy()
                self.arquivo_atual = caminho_para_salvar

                nome_arquivo = caminho_para_salvar.split("/")[-1]
                self.view.root.title(f"Drawable App - {nome_arquivo}")

                messagebox.showinfo(
                    "Sucesso", f"Desenho salvo em: {caminho_para_salvar}"
                )
                return True
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível salvar o arquivo: {e}")

    def carregar_desenho(self):
        """
        Carrega um desenho salvo em um arquivo Pickle.

        :return: None
        """
        if self.esta_alterado():
            resposta = messagebox.askyesnocancel(
                "Atenção",
                "Você tem desenhos não salvos. Deseja salvar antes de carregar?",
            )
            if resposta is True:
                if not self.salvar_desenho():
                    return
            elif resposta is False:
                pass
            else:
                return

        arquivo = filedialog.askopenfilename(
            filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")]
        )

        if arquivo:
            try:
                with open(arquivo, "rb") as f:
                    figuras_carregadas = pickle.load(f)

                self.historico.figuras.clear()
                self.historico.figuras_desfeitas.clear()
                self.historico._movimentacoes.clear()
                self.historico._movimentacoes_anteriores.clear()
                self.figuras_carregadas.clear()

                for figura in figuras_carregadas:
                    self.historico.adicionar(figura)
                    self.figuras_carregadas.append(figura)

                self.arquivo_atual = arquivo

                nome_arquivo = arquivo.split("/")[-1]
                self.view.root.title(f"Drawable App - {nome_arquivo}")

                self.desenhar_figuras()
                self.verifica_historico()
                messagebox.showinfo("Sucesso", "Desenho carregado com sucesso!")

            except Exception as e:
                messagebox.showerror(
                    "Erro", f"Não foi possível carregar o arquivo: {e}"
                )

    def fechar_app(self):
        """
        Fecha o aplicativo após verificar a existência de alterações não salvas.

        :return: None
        """
        if self.esta_alterado():
            resposta = messagebox.askyesnocancel(
                "Sair do Aplicativo",
                "Você tem desenhos não salvos. Deseja salvar antes de sair?",
            )

            if resposta is True:
                if self.salvar_desenho():
                    self.view.root.destroy()
            elif resposta is False:
                self.view.root.destroy()
        else:
            self.view.root.destroy()

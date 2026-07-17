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
    Poligono
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
        'Linha': Linha,
        'Rabisco': Rabisco,
        'Oval': Oval,
        'Circulo': Circulo,
        'Retangulo': Retangulo,
        'Triangulo': TrianguloEquilatero,
        'Triangulo Retangulo': TrianguloRetangulo,
        'Quadrado': Quadrado,
        'Pentagono': Pentagono,
        'Hexagono': Hexagono,
        'Poligono': Poligono
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
        return list(cls.MAPA_FIGURAS.keys())

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
        self.view.botao_cor_preenchimento.config(command=self.escolher_cor_do_preenchimento)
        self.view.botao_sem_preenchimento.config(command=self.remover_preenchimento)

        self.view.tipo_figura.trace_add('write', self.detecta_mudanca)
        self.view.lados_poligono.trace_add('write', self.detecta_mudanca)

        self.detecta_mudanca()

    def configurar_eventos(self):
        """
        Configura os eventos do mouse e os atalhos do teclado.

        :return: None
        """
        self.view.canvas.bind('<ButtonPress-1>', self.iniciar_figura_nova)
        self.view.canvas.bind('<B1-Motion>', self.atualizar_figura_nova)
        self.view.canvas.bind('<ButtonRelease-1>', self.incluir_figura_nova)
        self.view.canvas.bind('<Button-3>', self.finalizar_poligono)

        self.view.root.bind_all('<Control-z>', self.desfazer)
        self.view.root.bind_all('<Control-y>', self.refazer)
        self.view.canvas.focus_set()

    def atribuir_foco_canvas(self):
        """
        Configura o retorno do foco ao canvas após alterações nos seletores.

        :return: None
        """
        self.view.combo_lados.bind(
            "<<ComboboxSelected>>",
            lambda event: self.view.canvas.focus_set()
        )

        self.view.combo_espessura.bind(
            "<<ComboboxSelected>>",
            lambda event: self.view.canvas.focus_set()
        )

    def escolher_cor_da_borda(self):
        """
        Abre o seletor de cores e altera a cor da borda das próximas figuras.

        :return: None
        """
        cor = colorchooser.askcolor(title="Cor da borda")
        if cor[1] is not None:
            self.cor_da_borda = cor[1]
            self.view.indicador_borda.config(bg=self.cor_da_borda)

    def escolher_cor_do_preenchimento(self):
        """
        Abre o seletor de cores e altera a cor de preenchimento das próximas figuras.

        :return: None
        """
        corp = colorchooser.askcolor(title="Cor do preenchimento")
        if corp[1] is not None:
            self.cor_do_preenchimento = corp[1]
            self.view.indicador_preenchimento.config(bg=self.cor_do_preenchimento)

    def remover_preenchimento(self):
        """
        Remove a cor de preenchimento selecionada.

        :return: None
        """
        self.cor_do_preenchimento = ""
        self.view.indicador_preenchimento.config(bg="#D3D3D3")

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
        if hasattr(self.estado, 'finalizar'):
            self.estado.finalizar(self)

    def desenhar_figuras(self):
        """
        Desenha novamente todas as figuras armazenadas no histórico.

        :return: None
        """
        self.view.canvas.delete("all")
        for figura in self.historico.figuras:
            figura.desenhar(self.view.canvas)

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
        return (figura.values[0], figura.values[1]) == (figura.values[2], figura.values[3])

    def desfazer(self, *args):
        """
        Desfaz a última ação.

        Delega a ação ao estado atual.

        :param args: Argumentos opcionais enviados pelo evento de teclado.
        :return: None
        """
        self.estado.desfazer(self)

    def refazer(self, *args):
        """
        Refaz a última ação desfeita.

        Delega a ação ao estado atual.

        :param args: Argumentos opcionais enviados pelo evento de teclado.
        :return: None
        """
        self.estado.refazer(self)

    def esta_alterado(self):
        """
        Verifica se o desenho atual possui alterações ainda não salvas.

        :return: True quando existem alterações não salvas; False caso contrário.
        """
        if not self.historico.figuras:
            return False

        return (
                self.historico.figuras != self.figuras_carregadas or self.arquivo_atual is None
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
                filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")]
            )

        if caminho_para_salvar:
            try:
                with open(caminho_para_salvar, 'wb') as f:
                    pickle.dump(self.historico.figuras, f)

                self.figuras_carregadas = self.historico.figuras.copy()
                self.arquivo_atual = caminho_para_salvar

                nome_arquivo = caminho_para_salvar.split('/')[-1]
                self.view.root.title(f"Drawable App - {nome_arquivo}")

                messagebox.showinfo("Sucesso", f"Desenho salvo em: {caminho_para_salvar}")
                return True
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível salvar o arquivo: {e}")

    def carregar_desenho(self):
        """
        Carrega um desenho salvo em um arquivo Pickle.

        :return: None
        """
        if self.esta_alterado():
            resposta = messagebox.askyesnocancel("Atenção",
                                                 "Você tem desenhos não salvos. Deseja salvar antes de carregar?")
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
                with open(arquivo, 'rb') as f:
                    figuras_carregadas = pickle.load(f)

                self.historico.figuras.clear()
                self.historico.figuras_desfeitas.clear()
                self.figuras_carregadas.clear()

                for figura in figuras_carregadas:
                    self.historico.adicionar(figura)
                    self.figuras_carregadas.append(figura)

                self.arquivo_atual = arquivo

                nome_arquivo = arquivo.split('/')[-1]
                self.view.root.title(f"Drawable App - {nome_arquivo}")

                self.desenhar_figuras()
                self.verifica_historico()
                messagebox.showinfo("Sucesso", "Desenho carregado com sucesso!")

            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível carregar o arquivo: {e}")

    def fechar_app(self):
        """
        Fecha o aplicativo após verificar a existência de alterações não salvas.

        :return: None
        """
        if self.esta_alterado():
            resposta = messagebox.askyesnocancel("Sair do Aplicativo",
                                                 "Você tem desenhos não salvos. Deseja salvar antes de sair?")

            if resposta is True:
                if self.salvar_desenho():
                    self.view.root.destroy()
            elif resposta is False:
                self.view.root.destroy()
        else:
            self.view.root.destroy()

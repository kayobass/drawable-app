"""
Módulo responsável pelo controle do sistema de desenho.

Contém o controlador principal da aplicação, responsável por conectar
a visão ao histórico e às classes de figuras, além de controlar eventos,
comandos, criação de desenhos, persistência e fechamento do sistema.

@author: Matheuz Rozendo, Kayo Araujo
@version: OO.persiste.1
@since: OO.MVC.1
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


class DrawableController:
    """
    Controla as ações e os eventos do sistema de desenho.

    A classe faz a ligação entre a interface, o histórico e as classes das figuras.
    Ela também controla a escolha das ferramentas e cores, a criação dos desenhos,
    as funções de desfazer e refazer e o salvamento e carregamento dos arquivos.

    Para criar o controlador, é necessário informar a visão e o histórico.
    
    @author: Matheuz Rozendo, Kayo Araujo 
    @version: OO.persiste.1 
    @since: OO.MVC.1 
    @see: DrawableView, Historico
    
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
        Também define os valores iniciais das cores e das figuras e configura os comandos
        e eventos da interface.
        
        @param view: visão usada para acessar e atualizar a interface gráfica.
        @param historico: Histórico usado para guardar as figuras e controlar 
        as ações de desfazer e refazer.

        @return: None
        @see: configurar_comandos, configurar_eventos, atribuir_foco_canvas
        """
        self.view = view
        self.historico = historico

        self.cor_da_borda = "black"
        self.cor_do_preenchimento = ""

        self.figura_nova = None
        self.poligono_atual = None
        self.arquivo_atual = None
        self.figuras_carregadas = []

        self.configurar_comandos()
        self.configurar_eventos()
        self.atribuir_foco_canvas()


    @classmethod
    def figuras_disponiveis(cls):
        """
        Retorna os nomes das figuras disponíveis no sistema.

        Os nomes são obtidos a partir das chaves armazenadas em MAPA_FIGURAS.

        @return: Lista com os nomes das figuras disponíveis.
        @see: MAPA_FIGURAS
        """
        return list(cls.MAPA_FIGURAS.keys())


    @property
    def ferramenta(self):
        """
        Retorna a ferramenta selecionada atualmente na interface.

        @return: Nome da figura selecionada pelo usuário.
        """
        return self.view.tipo_figura.get()


    @property
    def espessura(self):
        """
        Retorna a espessura de linha selecionada na interface.

        @return: Valor da espessura selecionada pelo usuário.
        """
        return self.view.espessura.get()


    def configurar_comandos(self):
        """
        Associa os botões e controles da interface aos métodos do controlador.

        Configura os comandos de salvar, carregar, escolher cores, remover
        preenchimento e detectar mudanças nas opções selecionadas.

        @return: None
        @see: salvar_desenho, carregar_desenho, detecta_mudanca
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

        Os eventos são usados para criar as figuras e os atalhos Ctrl+Z e Ctrl+Y
        são usados para desfazer e refazer ações.

        @return: None
        @see: iniciar_figura_nova, atualizar_figura_nova, desfazer, refazer
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

        @return: None
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

        Caso o usuário cancele a seleção, a cor atual é mantida.

        @return: None
        """
        cor = colorchooser.askcolor(title="Cor da borda")
        if cor[1] is not None:
            self.cor_da_borda = cor[1]
            self.view.indicador_borda.config(bg=self.cor_da_borda)


    def escolher_cor_do_preenchimento(self):
        """
        Abre o seletor de cores e altera a cor de preenchimento das próximas figuras.

        Caso o usuário cancele a seleção, a cor atual é mantida.

        @return: None
        """
        corp = colorchooser.askcolor(title="Cor do preenchimento")
        if corp[1] is not None:
            self.cor_do_preenchimento = corp[1]
            self.view.indicador_preenchimento.config(bg=self.cor_do_preenchimento)


    def remover_preenchimento(self):
        """
        Remove a cor de preenchimento selecionada.

        As próximas figuras serão criadas sem preenchimento.

        @return: None
        """
        self.cor_do_preenchimento = ""
        self.view.indicador_preenchimento.config(bg="#D3D3D3")


    def detecta_mudanca(self, *args):
        """
        Atualiza a interface quando a ferramenta ou a quantidade de lados muda.

        Também cancela um polígono em construção e habilita ou desabilita
        os controles de preenchimento conforme a ferramenta selecionada.

        @param args: Informações enviadas automaticamente pelo Tkinter.
        @return: None
        """
        opcao_selecionada = self.ferramenta

        if self.poligono_atual is not None:
            self.poligono_atual = None
            self.desenhar_figuras()

        if opcao_selecionada == 'Poligono':
            self.view.label_lados.grid(row=0, column=2, sticky="w")
            self.view.combo_lados.grid(row=0, column=3, sticky="w")
        else:
            self.view.label_lados.grid_forget()
            self.view.combo_lados.grid_forget()

        if opcao_selecionada == 'Linha' or opcao_selecionada == 'Rabisco':
            self.view.botao_cor_preenchimento.config(state="disabled")
            self.view.botao_sem_preenchimento.config(state="disabled")
            self.view.indicador_preenchimento.config(bg="#D3D3D3")
            self.view.botao_cor_borda.config(text="Cor")
        else:
            self.view.botao_cor_preenchimento.config(state="normal")
            self.view.botao_sem_preenchimento.config(state="normal")
            self.view.indicador_preenchimento.config(bg=self.cor_do_preenchimento or "#D3D3D3")
            self.view.botao_cor_borda.config(text="Cor da borda")
            
            
    def verifica_historico(self):
        """
        Atualiza o estado do botão de salvar conforme o conteúdo do histórico.

        O botão é habilitado quando existem figuras e desabilitado quando
        o histórico está vazio.

        @return: None
        """
        if self.historico.figuras:
            self.view.botao_salvar.config(state="normal")
        else:
            self.view.botao_salvar.config(state="disabled")


    def iniciar_poligono(self, event):
        """
        Inicia a criação de um polígono ou adiciona um novo ponto ao polígono atual.

        Caso ainda não exista um polígono sendo criado, um novo é iniciado.
        O polígono é finalizado quando atinge a quantidade de lados escolhida
        pelo usuário.

        @param event: Evento do mouse que contém as coordenadas do clique.
        @return: None
        @see: finalizar_poligono, desenhar_figuras
        """
        if self.poligono_atual is None:
            self.poligono_atual = Poligono(
                [],
                self.cor_da_borda,
                self.cor_do_preenchimento,
                self.espessura
            )

        self.poligono_atual.adicionar_ponto(event.x, event.y)

        self.desenhar_figuras()
        self.poligono_atual.desenhar_pontos_do_poligono(self.view.canvas)

        if len(self.poligono_atual.values) == self.view.lados_poligono.get():
            self.finalizar_poligono(None)


    def iniciar_figura(self, event):
        """
        Inicia a criação de uma figura com base na ferramenta selecionada.

        Define as coordenadas iniciais da figura e utiliza as cores e a espessura
        escolhidas pelo usuário.

        @param event: Evento do mouse que contém as coordenadas iniciais da figura.
        @return: None
        @see: MAPA_FIGURAS
        """
        figura = self.MAPA_FIGURAS[self.ferramenta]

        valores_iniciais = (
            [(event.x, event.y)]
            if self.ferramenta == "Rabisco"
            else [event.x, event.y, event.x, event.y]
        )

        self.figura_nova = figura(
            valores_iniciais,
            self.cor_da_borda,
            self.cor_do_preenchimento,
            self.espessura
        )


    def iniciar_figura_nova(self, event):
        """
        Inicia uma nova figura de acordo com a ferramenta selecionada.

        Caso a ferramenta seja Polígono, inicia ou adiciona um ponto ao polígono.
        Para as outras ferramentas, inicia uma figura comum.

        @param event: Evento do mouse que contém as coordenadas do clique.
        @return: None
        @see: iniciar_poligono, iniciar_figura
        """
        if self.ferramenta == "Poligono":
            self.iniciar_poligono(event)
        else:
            self.iniciar_figura(event)


    def atualizar_figura_nova(self, event):
        """
        Atualiza a figura enquanto o usuário arrasta o mouse.

        No caso do rabisco, adiciona novos pontos ao desenho. Para as outras
        figuras, atualiza as coordenadas finais.

        @param event: Evento do mouse que contém a posição atual do cursor.
        @return: None
        @see: desenhar_figuras, desenhar_figura_nova
        """
        if self.ferramenta == 'Poligono':
            return

        if not self.figura_nova:
            return

        if isinstance(self.figura_nova, Rabisco):
            self.figura_nova.values.append((event.x, event.y))
        else:
            self.figura_nova.values[2] = event.x
            self.figura_nova.values[3] = event.y

        self.desenhar_figuras()
        self.desenhar_figura_nova()


    def incluir_figura_nova(self, event):
        """
        Finaliza a figura atual e a adiciona ao histórico.

        A figura só é adicionada quando estiver completa. Depois disso,
        a figura temporária é apagada e o canvas é atualizado.

        @param event: Evento gerado quando o botão do mouse é solto.
        @return: None
        @see: incompleta, verifica_historico, desenhar_figuras
        """
        if self.ferramenta == 'Poligono':
            return

        if self.figura_nova and not self.incompleta(self.figura_nova):
            self.historico.adicionar(self.figura_nova)
           
        self.figura_nova = None
        self.verifica_historico()
        self.desenhar_figuras()


    def finalizar_poligono(self, event):
        """
        Finaliza o polígono que está sendo criado.

        O polígono é adicionado ao histórico apenas quando possui pelo menos
        três pontos. Depois disso, o polígono atual é apagado e o canvas é atualizado.

        @param event: Evento do mouse ou None quando a finalização ocorre automaticamente.
        @return: None
        @see: iniciar_poligono, verifica_historico, desenhar_figuras
        """
        if self.poligono_atual is not None and len(self.poligono_atual.values) >= 3:
            self.historico.adicionar(self.poligono_atual)

        self.poligono_atual = None
        self.verifica_historico()
        self.desenhar_figuras()


    def desenhar_figuras(self):
        """
        Desenha novamente todas as figuras armazenadas no histórico.

        Primeiro limpa o canvas e depois percorre as figuras do histórico,
        desenhando cada uma delas.

        @return: None
        @see: Historico
        """
        self.view.canvas.delete("all")
        for figura in self.historico.figuras:
            figura.desenhar(self.view.canvas)


    def desenhar_figura_nova(self):
        """
        Desenha temporariamente a figura que está sendo criada.

        A figura temporária recebe uma linha tracejada para mostrar que ainda
        não foi adicionada ao histórico.

        @return: None
        @see: iniciar_figura, atualizar_figura_nova
        """
        if self.figura_nova:
            id_desenho = self.figura_nova.desenhar(self.view.canvas)
            if id_desenho:
                self.view.canvas.itemconfig(id_desenho, dash=(4, 2))


    def incompleta(self, figura):
        """
        Verifica se uma figura está incompleta.

        Um rabisco é considerado incompleto quando possui apenas um ponto.
        As outras figuras são consideradas incompletas quando as coordenadas
        iniciais e finais são iguais.

        @param figura: Figura que será verificada.
        @return: True se a figura estiver incompleta e False caso contrário.
        @see: Rabisco
        """
        if isinstance(figura, Rabisco):
            return len(figura.values) <= 1
        return (figura.values[0], figura.values[1]) == (figura.values[2], figura.values[3])


    def desfazer(self, *args):
        """
        Desfaz a última figura adicionada ao desenho.

        Caso exista um polígono ainda em construção, cancela apenas seu esboço.

        @param args: Argumentos opcionais enviados pelo evento de teclado.
        @return: None
        @see: Historico.desfazer
        """
        # Se estiver criando um polígono, cancela o esboço atual imediatamente
        if self.ferramenta == 'Poligono' and self.poligono_atual is not None:
            self.poligono_atual = None
            self.desenhar_figuras()
            return

        if self.historico.figuras:
            self.historico.desfazer()
            self.verifica_historico()
            self.desenhar_figuras()
            

    def refazer(self, *args):
        """
        Refaz a última figura anteriormente desfeita.

        Caso exista um polígono em construção, cancela seu esboço antes
        de executar a operação.

        @param args: Argumentos opcionais enviados pelo evento de teclado.
        @return: None
        @see: Historico.refazer
        """
        if self.ferramenta == 'Poligono' and self.poligono_atual is not None:
            self.poligono_atual = None
            self.desenhar_figuras()
            return

        if self.historico.figuras_desfeitas:
            self.historico.refazer()
            self.verifica_historico()
            self.desenhar_figuras()


    def esta_alterado(self):
        """
        Verifica se o desenho atual possui alterações ainda não salvas.

        @return: True quando existem alterações não salvas; False caso contrário.
        @since: OO.persiste.1
        """
        if not self.historico.figuras:
            return False
        
        return (
            self.historico.figuras != self.figuras_carregadas or self.arquivo_atual is None
        )


    def salvar_desenho(self):
        """
        Salva o desenho atual em um arquivo Pickle.

        Se o desenho já tiver sido salvo antes, o mesmo arquivo será atualizado.
        Caso contrário, o usuário poderá escolher onde salvar.

        @return: True se o desenho for salvo; None caso contrário.

        @since: OO.persiste.1
        @see: pickle.dump
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

        Antes de carregar, verifica se existem alterações que ainda não foram salvas.
        Depois, limpa o desenho atual, coloca as figuras carregadas no histórico
        e atualiza o canvas.

        @return: None
        @since: OO.persiste.1
        @see: salvar_desenho, pickle.load
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

        Caso existam alterações, oferece ao usuário as opções de salvar,
        sair sem salvar ou cancelar o fechamento.

        @return: None
        @since: OO.persiste.1
        @see: salvar_desenho, esta_alterado
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
            
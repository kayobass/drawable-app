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
        return list(cls.MAPA_FIGURAS.keys())


    @property
    def ferramenta(self):
        return self.view.tipo_figura.get()


    @property
    def espessura(self):
        return self.view.espessura.get()


    def configurar_comandos(self):
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
        self.view.canvas.bind('<ButtonPress-1>', self.iniciar_figura_nova)
        self.view.canvas.bind('<B1-Motion>', self.atualizar_figura_nova)
        self.view.canvas.bind('<ButtonRelease-1>', self.incluir_figura_nova)
        self.view.canvas.bind('<Button-3>', self.finalizar_poligono)

        self.view.root.bind_all('<Control-z>', self.desfazer)
        self.view.root.bind_all('<Control-y>', self.refazer)
        self.view.canvas.focus_set()


    def atribuir_foco_canvas(self):
        self.view.combo_lados.bind(
            "<<ComboboxSelected>>",
            lambda event: self.view.canvas.focus_set()
        )

        self.view.combo_espessura.bind(
            "<<ComboboxSelected>>",
            lambda event: self.view.canvas.focus_set()
        )


    def escolher_cor_da_borda(self):
        cor = colorchooser.askcolor(title="Cor da borda")
        if cor[1] is not None:
            self.cor_da_borda = cor[1]
            self.view.indicador_borda.config(bg=self.cor_da_borda)


    def escolher_cor_do_preenchimento(self):
        corp = colorchooser.askcolor(title="Cor do preenchimento")
        if corp[1] is not None:
            self.cor_do_preenchimento = corp[1]
            self.view.indicador_preenchimento.config(bg=self.cor_do_preenchimento)


    def remover_preenchimento(self):
        self.cor_do_preenchimento = ""
        self.view.indicador_preenchimento.config(bg="#D3D3D3")


    def detecta_mudanca(self, *args):
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
        if self.historico.figuras:
            self.view.botao_salvar.config(state="normal")
        else:
            self.view.botao_salvar.config(state="disabled")


    def iniciar_poligono(self, event):
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
        if self.ferramenta == "Poligono":
            self.iniciar_poligono(event)
        else:
            self.iniciar_figura(event)


    def atualizar_figura_nova(self, event):
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
        if self.ferramenta == 'Poligono':
            return

        if self.figura_nova and not self.incompleta(self.figura_nova):
            self.historico.adicionar(self.figura_nova)
           
        self.figura_nova = None
        self.verifica_historico()
        self.desenhar_figuras()


    def finalizar_poligono(self, event):
        if self.poligono_atual is not None and len(self.poligono_atual.values) >= 3:
            self.historico.adicionar(self.poligono_atual)

        self.poligono_atual = None
        self.verifica_historico()
        self.desenhar_figuras()


    def desenhar_figuras(self):
        self.view.canvas.delete("all")
        for figura in self.historico.figuras:
            figura.desenhar(self.view.canvas)


    def desenhar_figura_nova(self):
        if self.figura_nova:
            id_desenho = self.figura_nova.desenhar(self.view.canvas)
            if id_desenho:
                self.view.canvas.itemconfig(id_desenho, dash=(4, 2))


    def incompleta(self, figura):
        if isinstance(figura, Rabisco):
            return len(figura.values) <= 1
        return (figura.values[0], figura.values[1]) == (figura.values[2], figura.values[3])


    def desfazer(self, *args):
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
        # Se estiver criando um polígono, cancela o esboço atual se o usuário tentar refazer algo antigo
        if self.ferramenta == 'Poligono' and self.poligono_atual is not None:
            self.poligono_atual = None
            self.desenhar_figuras()
            return

        if self.historico.figuras_desfeitas:
            self.historico.refazer()
            self.verifica_historico()
            self.desenhar_figuras()


    def esta_alterado(self):
        return self.historico.figuras != self.figuras_carregadas


    def salvar_desenho(self):
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
                
                self.arquivo_atual = caminho_para_salvar
                
                nome_arquivo = caminho_para_salvar.split('/')[-1]
                self.view.root.title(f"Drawable App - {nome_arquivo}")
                
                messagebox.showinfo("Sucesso", f"Desenho salvo em: {caminho_para_salvar}")
                return True
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível salvar o arquivo: {e}")


    def carregar_desenho(self):
        if self.esta_alterado():
            resposta = messagebox.askyesnocancel("Atenção", 
                "Você tem desenhos não salvos. Deseja salvar antes de carregar?")
            if resposta is True:
                self.salvar_desenho()
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
            
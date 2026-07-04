from tkinter import *
from tkinter import colorchooser
from tkinter import ttk

# Importando as classes geométricas e historico
from models.figuras import *
from models.historico import Historico

class DrawableApp():
    MAPA_FIGURAS = {
        'Circulo': Circulo,
        'Linha': Linha,
        'Rabisco': Rabisco,
        'Oval': Oval,
        'Retangulo': Retangulo,
        'Triangulo': TrianguloEquilatero,
        'Triangulo Retangulo': TrianguloRetangulo,
        'Quadrado': Quadrado,
        'Pentagono': Pentagono,
        'Hexagono': Hexagono,
        'Poligono': Poligono
    }

    def __init__(self):
        self.historico = Historico()
        self.figura_nova = None  
        self.poligono_atual = None
        self.cor_da_borda = "black"
        self.cor_do_preenchimento = ""
        self.paddings = {'padx': 5, 'pady': 5} 

        # Inicialização da janela
        self.root = Tk()
        self.root.title('Drawable App')

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.frame = Frame(self.root)
        self.espessura = IntVar(value=2)
        self.lados_poligono = IntVar(value=3)

        # Chamando os métodos de criação dos widgets e eventos
        self.criar_widgets_selecao()
        self.criar_widgets_cores()
        self.criar_area_desenho()
        self.eventos_bind()

        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.rowconfigure(2, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.root.mainloop()

    def criar_widgets_selecao(self):
        self.label = ttk.Label(self.frame, text='Escolha a ferramenta de desenho:')
        self.label.grid(column=0, row=0, sticky=W, **self.paddings)

        self.frame_selecao = Frame(self.frame)
        self.frame_selecao.grid(column=1, row=0, sticky=W)

        self.tipo_figura_var = StringVar(self.root)
        self.option_menu = ttk.OptionMenu(
            self.frame_selecao, self.tipo_figura_var,
            'Linha', 'Linha', 'Rabisco', 'Retangulo', 'Oval', 'Circulo', 'Triangulo', 'Triangulo Retangulo', 'Quadrado', 'Pentagono', 'Hexagono', 'Poligono'
        )
        self.option_menu.pack(side="left")
        
        self.label_lados = ttk.Label(self.frame_selecao, text="  Lados:")
        self.combo_lados = ttk.Combobox(
            self.frame_selecao, 
            textvariable=self.lados_poligono, 
            values=list(range(3, 13)), 
            state="readonly", 
            width=3
        )
        # Retorna o foco ao Canvas ao mudar o lado
        self.combo_lados.bind(
            "<<ComboboxSelected>>",
            lambda event: self.canvas.focus_set()
        )
        self.combo_lados.current(0)
        
        self.tipo_figura_var.trace_add('write', self.opcao_mudou)
        self.lados_poligono.trace_add('write', self.opcao_mudou)

    def criar_widgets_cores(self):
        self.cores = ttk.Label(self.frame, text='Escolha as cores do desenho:')
        self.cores.grid(column=0, row=1, sticky=W, **self.paddings)

        self.frame_cores = Frame(self.frame)
        self.frame_cores.grid(column=1, row=1, sticky=W)

        self.botao_cor_borda = Button(self.frame_cores, text="Cor da borda", command=self.escolher_cor_da_borda)
        self.botao_cor_borda.pack(side="left", padx=0, pady=0)

        self.indicador_borda = Canvas(self.frame_cores, width=20, height=10, bg="black", highlightthickness=1, highlightbackground="gray")
        self.indicador_borda.pack(side="left", padx=5, pady=0)

        self.botao_cor_preenchimento = Button(self.frame_cores, text="Cor do preenchimento", command=self.escolher_cor_do_preenchimento)
        self.botao_cor_preenchimento.pack(side="left", padx=0, pady=0)

        self.indicador_preenchimento = Canvas(self.frame_cores, width=20, height=10, bg="#D3D3D3", highlightthickness=1, highlightbackground="gray")
        self.indicador_preenchimento.pack(side="left", padx=5, pady=0)

        self.botao_sem_preenchimento = Button(self.frame_cores, text="Sem preenchimento", command=self.remover_preenchimento)
        self.botao_sem_preenchimento.pack(side="left", padx=0, pady=0)

        ttk.Label(self.frame_cores, text="Espessura:").pack(side="left", padx=(10, 0))

        self.combo_espessura = ttk.Combobox(
            self.frame_cores,
            textvariable=self.espessura,
            values=list(range(1, 11)),
            state="readonly",
            width=2
        )
        # Retorna o foco ao Canvas ao mudar a espressura
        self.combo_espessura.bind(
            "<<ComboboxSelected>>",
            lambda event: self.canvas.focus_set()
        )
        self.combo_espessura.current(1)  
        self.combo_espessura.pack(side="left")
        
        self.opcao_mudou()

    def criar_area_desenho(self):
        self.canvas = Canvas(self.frame, bg='white', width=600, height=600)
        self.canvas.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="nsew",
            **self.paddings
        )

    def escolher_cor_da_borda(self):
        cor = colorchooser.askcolor(title="Cor da borda")
        if cor[1] is not None:
            self.cor_da_borda = cor[1]
            self.indicador_borda.config(bg=self.cor_da_borda)

    def escolher_cor_do_preenchimento(self):
        corp = colorchooser.askcolor(title="Cor do preenchimento")
        if corp[1] is not None:
            self.cor_do_preenchimento = corp[1]
            self.indicador_preenchimento.config(bg=self.cor_do_preenchimento)

    def remover_preenchimento(self):
        self.cor_do_preenchimento = ""
        self.indicador_preenchimento.config(bg="#D3D3D3")

    def iniciar_figura_nova(self, event):
        opcao = self.tipo_figura_var.get()
        if opcao == 'Poligono':
            if self.poligono_atual is None:
                self.poligono_atual = Poligono([], self.cor_da_borda, self.cor_do_preenchimento, self.espessura.get())

            self.poligono_atual.adicionar_ponto(event.x, event.y)
            self.desenhar_figuras()
            self.poligono_atual.desenhar_pontos_do_poligono(self.canvas)
            
            if len(self.poligono_atual.values) == self.lados_poligono.get():
                self.finalizar_poligono(None)
            return
        
        figura = self.MAPA_FIGURAS.get(opcao)
        valores_iniciais = [(event.x, event.y)] if opcao == 'Rabisco' else [event.x, event.y, event.x, event.y]
        self.figura_nova = figura(valores_iniciais, self.cor_da_borda, self.cor_do_preenchimento, self.espessura.get())

    def atualizar_figura_nova(self, event):
        if self.tipo_figura_var.get() == 'Poligono':
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
        if self.tipo_figura_var.get() == 'Poligono':
            return 
        
        if self.figura_nova and not self.incompleta(self.figura_nova):  
            self.historico.adicionar(self.figura_nova)
        self.figura_nova = None
        self.desenhar_figuras()

    def finalizar_poligono(self, event):
        if self.poligono_atual is not None and len(self.poligono_atual.values) >= 3:
            self.historico.adicionar(self.poligono_atual)
        
        self.poligono_atual = None
        self.desenhar_figuras()

    def desenhar_figuras(self):
        self.canvas.delete("all")
        for figura in self.historico.figuras:
            figura.desenhar(self.canvas)

    def desenhar_figura_nova(self):
        if self.figura_nova:
            id_desenho = self.figura_nova.desenhar(self.canvas)
            if id_desenho:
                self.canvas.itemconfig(id_desenho, dash=(4, 2))

    def incompleta(self, figura):
        if isinstance(figura, Rabisco):
            return len(figura.values) <= 1
        return (figura.values[0], figura.values[1]) == (figura.values[2], figura.values[3])
        
    def eventos_bind(self):
        self.canvas.bind('<ButtonPress-1>', self.iniciar_figura_nova)
        self.canvas.bind('<B1-Motion>', self.atualizar_figura_nova)
        self.canvas.bind('<ButtonRelease-1>', self.incluir_figura_nova)
        self.canvas.bind('<Button-3>', self.finalizar_poligono)

        self.canvas.bind('<Control-z>', self.desfazer)
        self.canvas.bind('<Control-y>', self.refazer)
        self.canvas.focus_set()

    def desfazer(self, *args):
        # Se estiver criando um polígono, cancela o esboço atual imediatamente
        if self.tipo_figura_var.get() == 'Poligono' and self.poligono_atual is not None:
            self.poligono_atual = None
            self.desenhar_figuras()
            return

        if self.historico.figuras:
            self.historico.desfazer()
            self.desenhar_figuras()

    def refazer(self, *args):
        # Se estiver criando um polígono, cancela o esboço atual se o usuário tentar refazer algo antigo
        if self.tipo_figura_var.get() == 'Poligono' and self.poligono_atual is not None:
            self.poligono_atual = None
            self.desenhar_figuras()
            return

        if self.historico.figuras_desfeitas:
            self.historico.refazer()
            self.desenhar_figuras()

    def opcao_mudou(self, *args):
        opcao_selecionada = self.tipo_figura_var.get()
        
        if self.poligono_atual is not None:
            self.poligono_atual = None
            self.desenhar_figuras()

        if opcao_selecionada == 'Poligono':
            self.label_lados.pack(side="left")
            self.combo_lados.pack(side="left")
        else:
            self.label_lados.pack_forget()
            self.combo_lados.pack_forget()

        if opcao_selecionada == 'Linha' or opcao_selecionada == 'Rabisco':
            self.botao_cor_preenchimento.config(state="disabled")
            self.botao_sem_preenchimento.config(state="disabled")
            self.indicador_preenchimento.config(bg="#D3D3D3")
            self.botao_cor_borda.config(text="Cor")
        else:
            self.botao_cor_preenchimento.config(state="normal")
            self.botao_sem_preenchimento.config(state="normal")
            self.indicador_preenchimento.config(bg=self.cor_do_preenchimento or "#D3D3D3")
            self.botao_cor_borda.config(text="Cor da borda")

def main():
    app = DrawableApp()

if __name__ == "__main__":
    main()
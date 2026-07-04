from tkinter import *
from tkinter import ttk
from tkinter import colorchooser

class DrawableView:
    def __init__(self):
        self.root = Tk()
        self.root.title('Drawable App')
        self.frame = Frame(self.root)
        self.espessura = IntVar(value=2)
        self.lados_poligono = IntVar(value=3)
        self.cor_da_borda = "black"
        self.cor_do_preenchimento = ""
        self.paddings = {'padx': 5, 'pady': 5}
        self.criar_widgets_selecao()
        self.criar_widgets_cores()
        self.criar_area_desenho()
        self.frame.pack()

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
        self.combo_espessura.current(1)  
        self.combo_espessura.pack(side="left")
        
        self.opcao_mudou()

    def criar_area_desenho(self):
        self.canvas = Canvas(self.frame, bg='white', width=600, height=600)
        self.canvas.grid(column=0, row=2, columnspan=2, sticky=W, **self.paddings)

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

    def opcao_mudou(self, *args):
        opcao_selecionada = self.tipo_figura_var.get()
        
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
    
    def eventos_bind(self, controller):
        self.canvas.bind('<ButtonPress-1>', controller.iniciar_figura_nova)
        self.canvas.bind('<B1-Motion>', controller.atualizar_figura_nova)
        self.canvas.bind('<ButtonRelease-1>', controller.incluir_figura_nova)
        self.canvas.bind('<Button-3>', controller.finalizar_poligono)

        self.canvas.bind('<Control-z>', controller.desfazer)
        self.canvas.bind('<Control-y>', controller.refazer)
        self.canvas.focus_set()
    
    def iniciar(self):
        self.root.mainloop()
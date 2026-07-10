from tkinter import *
from tkinter import ttk

class DrawableView:
    def __init__(self, figuras):
        self.figuras = figuras
        
        self.root = Tk()
        self.root.title("Drawable App")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        self.paddings = {"padx": 5, "pady": 5}
        
        self.frame = Frame(self.root)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.rowconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)
        self.frame.columnconfigure(4, weight=0)
        
        self.criar_widgets_selecao()
        self.criar_widgets_personalizacao()
        self.criar_area_desenho()

    def criar_widgets_selecao(self):
        self.label = ttk.Label(
            self.frame,
            text="Escolha a ferramenta:"
        )
        self.label.grid(
            row=0,
            column=0,
            sticky="w",
            **self.paddings
        )
        self.tipo_figura = StringVar(value="Linha")
        self.option_menu = ttk.OptionMenu(
            self.frame,
            self.tipo_figura,
            self.figuras[0],
            *self.figuras
        )
        self.option_menu.grid(
            row=0,
            column=1,
            sticky="w",
            **self.paddings
        )
        self.label_lados = ttk.Label(self.frame, text="  Lados:")
        self.label_lados.grid(
            row=0,
            column=2,
            sticky="w",
            **self.paddings
        )
        self.lados_poligono = IntVar(value=3)
        self.combo_lados = ttk.Combobox(
            self.frame,
            textvariable=self.lados_poligono,
            values=list(range(3, 13)),
            state="readonly",
            width=3
        )
        self.combo_lados.grid(
            row=0,
            column=3,
            sticky="w",
            **self.paddings
        )
        
        self.botao_salvar = Button(
            self.frame,
            text="Salvar",
            state="disabled"
        )
        self.botao_salvar.grid(
            row=0,
            column=4,
            sticky="e",
            padx=(5, 0),
            pady=5
        )
        
        self.botao_carregar = Button(
            self.frame,
            text="Carregar"
        )
        self.botao_carregar.grid(
            row=0,
            column=5,
            sticky="e",
            padx=(5, 5),
            pady=5
        )

    def criar_widgets_personalizacao(self):
        self.label_cores = ttk.Label(
            self.frame,
            text="Escolha as cores do desenho:"
        )
        self.label_cores.grid(
            row=1,
            column=0,
            sticky="w",
            **self.paddings
        )
        self.frame_cores = Frame(self.frame)
        self.frame_cores.grid(
            row=1,
            column=1,
            columnspan=5,
            sticky="w",
            **self.paddings
        )
        self.botao_cor_borda = Button(
            self.frame_cores,
            text="Cor da borda"
        )
        self.botao_cor_borda.pack(side="left", padx=0, pady=0)
        self.indicador_borda = Canvas(
            self.frame_cores,
            width=20,
            height=10,
            bg="black",
            highlightthickness=1,
            highlightbackground="gray"
        )
        self.indicador_borda.pack(side="left", padx=5, pady=0)
        self.botao_cor_preenchimento = Button(
            self.frame_cores,
            text="Cor do preenchimento"
        )
        self.botao_cor_preenchimento.pack(side="left", padx=0, pady=0)
        self.indicador_preenchimento = Canvas(
            self.frame_cores,
            width=20,
            height=10,
            bg="#D3D3D3",
            highlightthickness=1,
            highlightbackground="gray"
        )
        self.indicador_preenchimento.pack(side="left", padx=5, pady=0)
        self.botao_sem_preenchimento = Button(
            self.frame_cores,
            text="Sem preenchimento"
        )
        self.botao_sem_preenchimento.pack(side="left", padx=0, pady=0)
        ttk.Label(self.frame_cores, text="Espessura:").pack(side="left", padx=(10, 0))
        self.espessura = IntVar(value=2)
        self.combo_espessura = ttk.Combobox(
            self.frame_cores,
            values=list(range(1, 11)),
            textvariable=self.espessura,
            state="readonly",
            width=2
        )
        self.combo_espessura.pack(side="left")

    def criar_area_desenho(self):
        self.canvas = Canvas(
            self.frame,
            bg="white",
            width=600,
            height=600
        )
        self.canvas.grid(
            row=2,
            column=0,
            columnspan=6,
            sticky="nsew",
            **self.paddings
        )

    def mainloop(self):
        self.root.mainloop()
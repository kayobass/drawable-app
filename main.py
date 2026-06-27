from tkinter import *
from tkinter import colorchooser
from tkinter import ttk

# Importando a classes geométricas

from circulo import Circulo
from linha import Linha
from retangulo import Retangulo
from oval import Oval
from rabisco import Rabisco


class DrawableApp():
    # Dicionário para mapear a string do menu para a classe real
    MAPA_FIGURAS = {
        'Linha': Linha,
        'Retangulo': Retangulo,
        'Oval': Oval,
        'Circulo': Circulo,
        'Rabisco': Rabisco
    }

    def __init__(self):
        self.historico_figuras = []  # Todas as figuras desenhadas
        self.figuras_desfeitas = []  # Figuras que foram desfeitas (para refazer)
        self.figura_nova = None  # Figura que está sendo desenhada, mas ainda não foi incluída em figuras
        self.cor_da_borda = "black"
        self.cor_do_preenchimento = ""
        self.paddings = {'padx': 5, 'pady': 5 } # Widgets arranjados com Layout grid dentro de frame


        # Inicialização da janela
        self.root = Tk()
        self.root.title('Drawable App')
        self.frame = Frame(self.root)
        self.espessura = IntVar(value=1)

        # Chamandos os métodos de criação dos widgets e eventos
        self.criar_widgets_selecao()
        self.criar_widgets_cores()
        self.criar_area_desenho()
        self.eventos_bind()

        self.frame.pack()
        self.root.mainloop()


    # Cria os elementos de escolha de ferramentas
    def criar_widgets_selecao(self):
        self.label = ttk.Label(self.frame, text='Escolha a ferramenta de desenho:')
        self.label.grid(column=0, row=0, sticky=W, **self.paddings)

        self.tipo_figura_var = StringVar(self.root)
        self.option_menu = ttk.OptionMenu(
            self.frame, self.tipo_figura_var,
            'Linha', 'Linha', 'Rabisco', 'Retangulo', 'Oval', 'Circulo'
        )
        self.option_menu.grid(column=1, row=0, sticky=W, **self.paddings)
        
        self.tipo_figura_var.trace_add('write', self.opcao_mudou)


    # Cria o painel de seleção e indicação de cores
    def criar_widgets_cores(self):
        self.cores = ttk.Label(self.frame, text='Escolha as cores do desenho:')
        self.cores.grid(column=0, row=1, sticky=W, **self.paddings)

        self.frame_cores = Frame(self.frame)
        self.frame_cores.grid(column=1, row=1, sticky=W)

        # Configuração dos botões e indicadores de borda/preenchimento
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
        self.combo_espessura.current(1)  # Define o valor inicial como 2
        self.combo_espessura.pack(side="left")
        
        self.opcao_mudou()


    # Cria o Canvas principal onde os desenhos acontecem
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


    # Quando mouse é pressionado e cria um objeto da figura escolhida
    def iniciar_figura_nova(self, event):
        opcao = self.tipo_figura_var.get()
        figura = self.MAPA_FIGURAS.get(opcao)

        valores_iniciais = [(event.x, event.y)] if opcao == 'Rabisco' else [event.x, event.y, event.x, event.y]

        self.figura_nova = figura(valores_iniciais, self.cor_da_borda, self.cor_do_preenchimento, self.espessura.get())


    # Quando mouse é movido com o botão pressionado
    def atualizar_figura_nova(self, event):
        if not self.figura_nova:
            return

        if isinstance(self.figura_nova, Rabisco):
            self.figura_nova.values.append((event.x, event.y))
        else:
            self.figura_nova.values[2] = event.x
            self.figura_nova.values[3] = event.y

        self.desenhar_figuras()
        self.desenhar_figura_nova()


    # Quando mouse é solto
    def incluir_figura_nova(self, event):
        if self.figura_nova and not self.incompleta(self.figura_nova):  # Para evitar incluir figuras incompletas, como uma linha sem comprimento ou um rabisco com um único ponto
            self.historico_figuras.append(self.figura_nova)
            self.figuras_desfeitas.clear()  # Limpa o histórico de refazer, pois uma nova figura foi adicionada
        self.figura_nova = None
        self.desenhar_figuras()


    def desenhar_figuras(self):
        self.canvas.delete("all")
        for figura in self.historico_figuras:
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
        # Eventos de mouse associados ao canvas - com seus callbacks
        self.canvas.bind('<ButtonPress-1>', self.iniciar_figura_nova)
        self.canvas.bind('<B1-Motion>', self.atualizar_figura_nova)
        self.canvas.bind('<ButtonRelease-1>', self.incluir_figura_nova)

        # Eventos de teclado para desfazer/refazer
        self.canvas.bind('<Control-z>', self.desfazer)
        self.canvas.bind('<Control-y>', self.refazer)

        # Focar no canvas para capturar eventos de teclado
        self.canvas.focus_set()


    # Função para desfazer (ctrl+z)
    def desfazer(self, *args):
        if self.historico_figuras:
            figura = self.historico_figuras.pop()
            self.figuras_desfeitas.append(figura)
            self.desenhar_figuras()


    # Função para refazer (ctrl+y)
    def refazer(self, *args):
        if self.figuras_desfeitas:
            figura = self.figuras_desfeitas.pop()
            self.historico_figuras.append(figura)
            self.desenhar_figuras()


    # Verificação de alteração no valor do menu
    def opcao_mudou(self, *args):
        opcao_selecionada = self.tipo_figura_var.get()
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


# Função principal para iniciar a aplicação

def main():
    app = DrawableApp()

if __name__ == "__main__":
    main()

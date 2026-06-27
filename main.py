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
    def __init__(self):
        # Variáveis que antes eram globais e agora ficam dentro da classe
        self.historico_figuras = []  # Todas as figuras desenhadas
        self.figuras_desfeitas = []  # Figuras que foram desfeitas (para refazer)
        self.figura_nova = None  # Figura que está sendo desenhada, mas ainda não foi incluída em figuras
        self.cor_da_borda = "black"
        self.cor_do_preenchimento = ""

        self.root = Tk()
        self.root.title('Drawable App')
        self.frame = Frame(self.root)

        # Widgets arranjados com Layout grid dentro de frame
        self.paddings = {'padx': 5, 'pady': 5}

        # Label
        self.label = ttk.Label(self.frame, text='Escolha a ferramenta de desenho:')
        self.label.grid(column=0, row=0, sticky=W, **self.paddings)

        # Label para cores
        self.cores = ttk.Label(self.frame, text='Escolha as cores do desenho:')
        self.cores.grid(column=0, row=1, sticky=W, **self.paddings)

        # Option menu
        self.tipo_figura_var = StringVar(self.root)  # Guarda o tipo de figura selecionado no option menu

        self.option_menu = ttk.OptionMenu(self.frame, self.tipo_figura_var,
                                    'Linha', 'Linha', 'Rabisco', 'Retangulo', 'Oval', 'Circulo')
        self.option_menu.grid(column=1, row=0, sticky=W, **self.paddings)

        # Frame para as cores
        self.frame_cores = Frame(self.frame)
        self.frame_cores.grid(column=1, row=1, sticky=W)

        # Botao de cor da borda
        self.botao_cor_borda = Button(self.frame_cores, text="Cor da borda", command=self.escolher_cor_da_borda)
        self.botao_cor_borda.pack(side="left", padx=0, pady=0)

        # Indicador da cor da borda
        self.indicador_borda = Canvas(self.frame_cores, width=20, height=10, bg="black", highlightthickness=1, highlightbackground="gray")
        self.indicador_borda.pack(side="left", padx=5, pady=0)

        # Botao de cor do preenchimento
        self.botao_cor_preenchimento = Button(self.frame_cores, text="Cor do preenchimento", command=self.escolher_cor_do_preenchimento)
        self.botao_cor_preenchimento.pack(side="left", padx=0, pady=0)

        # Indicador da cor do preenchimento
        self.indicador_preenchimento = Canvas(self.frame_cores, width=20, height=10, bg="#D3D3D3", highlightthickness=1,
                                        highlightbackground="gray")
        self.indicador_preenchimento.pack(side="left", padx=5, pady=0)

        # Botao para não ter preenchimento
        self.botao_sem_preenchimento = Button(self.frame_cores, text="Sem preenchimento", command=self.remover_preenchimento)
        self.botao_sem_preenchimento.pack(side="left", padx=0, pady=0)

        self.tipo_figura_var.trace_add('write', self.opcao_mudou)
        self.opcao_mudou()

        # Área de desenho
        self.canvas = Canvas(self.frame, bg='white', width=600, height=600)
        self.canvas.grid(column=0, row=2, columnspan=2, sticky=W, **self.paddings)

        self.frame.pack()

        # Eventos de mouse associados ao canvas - com seus callbacks
        self.canvas.bind('<ButtonPress-1>', self.iniciar_figura_nova)
        self.canvas.bind('<B1-Motion>', self.atualizar_figura_nova)
        self.canvas.bind('<ButtonRelease-1>', self.incluir_figura_nova)

        # Eventos de teclado para desfazer/refazer
        self.canvas.bind('<Control-z>', self.desfazer)
        self.canvas.bind('<Control-y>', self.refazer)

        # Focar no canvas para capturar eventos de teclado
        self.canvas.focus_set()

        self.root.mainloop()


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


    # Quando mouse é pressionado
    def iniciar_figura_nova(self, event):
        if self.tipo_figura_var.get() == 'Linha':
            self.figura_nova = ("linha", (event.x, event.y, event.x, event.y))
        elif self.tipo_figura_var.get() == 'Retangulo':
            self.figura_nova = ('retangulo', (event.x, event.y, event.x, event.y))
        elif self.tipo_figura_var.get() == 'Oval':
            self.figura_nova = ('oval', (event.x, event.y, event.x, event.y))
        elif self.tipo_figura_var.get() == 'Circulo':
            self.figura_nova = ('circulo', (event.x, event.y, event.x, event.y))
        else:
            self.figura_nova = ("rabisco", [(event.x, event.y)])


    # Quando mouse é movido com o botão pressionado
    def atualizar_figura_nova(self, event):
        if self.figura_nova[0] == "rabisco":
            self.figura_nova[1].append((event.x, event.y))
        elif self.figura_nova[0] == "retangulo":
            self.figura_nova = ("retangulo", (self.figura_nova[1][0], self.figura_nova[1][1], event.x, event.y))
        elif self.figura_nova[0] == "oval":
            self.figura_nova = ("oval", (self.figura_nova[1][0], self.figura_nova[1][1], event.x, event.y))
        elif self.figura_nova[0] == "circulo":
            self.figura_nova = ("circulo", (self.figura_nova[1][0], self.figura_nova[1][1], event.x, event.y))
        else:  # figura_nova[0] == "linha"
            self.figura_nova = ("linha", (self.figura_nova[1][0], self.figura_nova[1][1], event.x, event.y))
        self.desenhar_figuras()
        self.desenhar_figura_nova()

    # Cria um objeto da figura escolhida, substituindo o uso de tuplas no histórico
    def criar_figura(self, fig, values, cor_borda, cor_preenchimento):
        if fig == "linha":
            return Linha(values, cor_borda, cor_preenchimento)
        elif fig == "retangulo":
            return Retangulo(values, cor_borda, cor_preenchimento)
        elif fig == "oval":
            return Oval(values, cor_borda, cor_preenchimento)
        elif fig == "circulo":
            return Circulo(values, cor_borda, cor_preenchimento)
        else:
            return Rabisco(values, cor_borda, cor_preenchimento)


    # Quando mouse é solto
    def incluir_figura_nova(self, event):
        if not self.incompleta(
                self.figura_nova):  # Para evitar incluir figuras incompletas, como uma linha sem comprimento ou um rabisco com um único ponto
            fig, values = self.figura_nova
            figura = self.criar_figura(fig, values, self.cor_da_borda, self.cor_do_preenchimento)
            self.historico_figuras.append(figura)
            self.figuras_desfeitas.clear()
        self.desenhar_figuras()


    def desenhar_figuras(self):
        self.canvas.delete("all")
        for figura in self.historico_figuras:
            figura.desenhar(self.canvas)


    def desenhar_figura_nova(self):
        fig, values = self.figura_nova
        if fig == "linha":
            self.canvas.create_line(values[0], values[1], values[2], values[3], dash=(4, 2), fill=self.cor_da_borda)
        elif fig == "retangulo":
            self.canvas.create_rectangle(values[0], values[1], values[2], values[3], dash=(4, 2), outline=self.cor_da_borda,
                                    fill=self.cor_do_preenchimento)
        elif fig == "oval":
            self.canvas.create_oval(values[0], values[1], values[2], values[3], dash=(4, 2), outline=self.cor_da_borda,
                            fill=self.cor_do_preenchimento)
        elif fig == "circulo":
            circulo = Circulo(values, self.cor_da_borda, self.cor_do_preenchimento)
            a, b, c, d = circulo.oval_em_circulo(values)
            self.canvas.create_oval(a, b, c, d, dash=(4, 2), outline=self.cor_da_borda, fill=self.cor_do_preenchimento)
        else:  # fig == "rabisco"
            self.canvas.create_line(values, dash=(4, 2), fill=self.cor_da_borda)


    def incompleta(self, figura):
        fig, values = figura
        if fig == "linha" or fig == 'retangulo' or fig == 'oval' or fig == 'circulo':
            return (values[0], values[1]) == (values[2], values[3])
        else:  # fig == "rabisco"
            return len(values) <= 1


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
        else:
            self.botao_cor_preenchimento.config(state="normal")
            self.botao_sem_preenchimento.config(state="normal")
            self.indicador_preenchimento.config(bg=self.cor_do_preenchimento or "#D3D3D3")

# Função principal para iniciar a aplicação

def main():
    app = DrawableApp()

if __name__ == "__main__":
    main()

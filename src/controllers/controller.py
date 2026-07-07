from tkinter import colorchooser


from models.linha import Linha
from models.rabisco import Rabisco
from models.circulo import Circulo
from models.oval import Oval
from models.quadrado import Quadrado
from models.retangulo import Retangulo
from models.triangulo_equilatero import TrianguloEquilatero
from models.triangulo_retangulo import TrianguloRetangulo
from models.pentagono import Pentagono
from models.hexagono import Hexagono
from models.poligono import Poligono



class DrawableController:
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

    def __init__(self, view, historico):
        self.view = view
        self.historico = historico

        self.cor_da_borda = "black"
        self.cor_do_preenchimento = ""

        self.figura_nova = None
        self.poligono_atual = None

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
        self.view.botao_cor_borda.config(command=self.escolher_cor_da_borda)
        self.view.botao_cor_preenchimento.config(command=self.escolher_cor_do_preenchimento)
        self.view.botao_sem_preenchimento.config(command=self.remover_preenchimento)

        self.view.tipo_figura.trace_add('write', self.opcao_mudou)
        self.view.lados_poligono.trace_add('write', self.opcao_mudou)

        self.opcao_mudou()

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

    def opcao_mudou(self, *args):
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
        self.desenhar_figuras()

    def finalizar_poligono(self, event):
        if self.poligono_atual is not None and len(self.poligono_atual.values) >= 3:
            self.historico.adicionar(self.poligono_atual)

        self.poligono_atual = None
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
            self.desenhar_figuras()

    def refazer(self, *args):
        # Se estiver criando um polígono, cancela o esboço atual se o usuário tentar refazer algo antigo
        if self.ferramenta == 'Poligono' and self.poligono_atual is not None:
            self.poligono_atual = None
            self.desenhar_figuras()
            return

        if self.historico.figuras_desfeitas:
            self.historico.refazer()
            self.desenhar_figuras()

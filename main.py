from tkinter import *
from tkinter import colorchooser
from tkinter import ttk


def escolher_cor_da_borda():
    global cor_da_borda
    cor = colorchooser.askcolor(title="Cor da borda")
    if cor[1] is not None:
        cor_da_borda = cor[1]
        indicador_borda.config(bg=cor_da_borda)


def escolher_cor_do_preenchimento():
    global cor_do_preenchimento
    corp = colorchooser.askcolor(title="Cor do preenchimento")
    if corp[1] is not None:
        cor_do_preenchimento = corp[1]
        indicador_preenchimento.config(bg=cor_do_preenchimento)


def remover_preenchimento():
    global cor_do_preenchimento
    cor_do_preenchimento = ""


# Quando mouse é pressionado
def iniciar_figura_nova(event):
    global figura_nova
    if tipo_figura_var.get() == 'Linha':
        figura_nova = ("linha", (event.x, event.y, event.x, event.y))
    elif tipo_figura_var.get() == 'Retangulo':
        figura_nova = ('retangulo', (event.x, event.y, event.x, event.y))
    elif tipo_figura_var.get() == 'Oval':
        figura_nova = ('oval', (event.x, event.y, event.x, event.y))
    elif tipo_figura_var.get() == 'Circulo':
        figura_nova = ('circulo', (event.x, event.y, event.x, event.y))
    else:
        figura_nova = ("rabisco", [(event.x, event.y)])


# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova
    if figura_nova[0] == "rabisco":
        figura_nova[1].append((event.x, event.y))
    elif figura_nova[0] == "retangulo":
        figura_nova = ("retangulo", (figura_nova[1][0], figura_nova[1][1], event.x, event.y))
    elif figura_nova[0] == "oval":
        figura_nova = ("oval", (figura_nova[1][0], figura_nova[1][1], event.x, event.y))
    elif figura_nova[0] == "circulo":
        figura_nova = ("circulo", (figura_nova[1][0], figura_nova[1][1], event.x, event.y))
    else:  # figura_nova[0] == "linha"
        figura_nova = ("linha", (figura_nova[1][0], figura_nova[1][1], event.x, event.y))
    desenhar_figuras()
    desenhar_figura_nova()


# Quando mouse é solto
def incluir_figura_nova(event):
    global historico_figuras, figuras_desfeitas
    if not incompleta(
            figura_nova):  # para evitar incluir figuras incompletas, como uma linha sem comprimento ou um rabisco com um único ponto
        fig, values = figura_nova
        historico_figuras.append((fig, values, cor_da_borda, cor_do_preenchimento))
        figuras_desfeitas.clear()
    desenhar_figuras()


# Utilizando a ideia de transformar o retangulo diretor em quadrado para desenhar um circulo
def oval_em_circulo(values):
    a, b, c, d = values
    largura = c - a
    altura = d - b
    tamanho = min(abs(largura), abs(altura))
    if largura < 0:
        c = a - tamanho
    else:
        c = a + tamanho
    if altura < 0:
        d = b - tamanho
    else:
        d = b + tamanho
    return a, b, c, d


def desenhar_figuras():
    canvas.delete("all")
    for fig, values, cor, cor_preenchimento in historico_figuras:
        if fig == "linha":
            canvas.create_line(values[0], values[1], values[2], values[3], fill=cor)
        elif fig == "retangulo":
            canvas.create_rectangle(values[0], values[1], values[2], values[3], outline=cor, fill=cor_preenchimento)
        elif fig == "oval":
            canvas.create_oval(values[0], values[1], values[2], values[3], outline=cor, fill=cor_preenchimento)
        elif fig == "circulo":
            a, b, c, d = oval_em_circulo(values)
            canvas.create_oval(a, b, c, d, outline=cor, fill=cor_preenchimento)
        else:  # fig == "rabisco"
            canvas.create_line(values, fill=cor)


def desenhar_figura_nova():
    fig, values = figura_nova
    if fig == "linha":
        canvas.create_line(values[0], values[1], values[2], values[3], dash=(4, 2), fill=cor_da_borda)
    elif fig == "retangulo":
        canvas.create_rectangle(values[0], values[1], values[2], values[3], dash=(4, 2), outline=cor_da_borda,
                                fill=cor_do_preenchimento)
    elif fig == "oval":
        canvas.create_oval(values[0], values[1], values[2], values[3], dash=(4, 2), outline=cor_da_borda,
                           fill=cor_do_preenchimento)
    elif fig == "circulo":
        a, b, c, d = oval_em_circulo(values)
        canvas.create_oval(a, b, c, d, dash=(4, 2), outline=cor_da_borda, fill=cor_do_preenchimento)
    else:  # fig == "rabisco"
        canvas.create_line(values, dash=(4, 2), fill=cor_da_borda)


def incompleta(figura):
    fig, values = figura
    if fig == "linha" or fig == 'retangulo' or fig == 'oval' or fig == 'circulo':
        return (values[0], values[1]) == (values[2], values[3])
    else:  # fig == "rabisco"
        return len(values) <= 1


# função para desfazer (ctrl+z)
def desfazer():
    global historico_figuras, figuras_desfeitas
    if historico_figuras:
        figura = historico_figuras.pop()
        figuras_desfeitas.append(figura)
        desenhar_figuras()


# função para refazer (ctrl+y)
def refazer():
    global historico_figuras, figuras_desfeitas
    if figuras_desfeitas:
        figura = figuras_desfeitas.pop()
        historico_figuras.append(figura)
        desenhar_figuras()


# ******* MAIN *******#

historico_figuras = []  # Todas as figuras desenhadas
figuras_desfeitas = []  # Figuras que foram desfeitas (para refazer)
figura_nova = None  # Figura que está sendo desenhada, mas ainda não foi incluída em figuras
cor_da_borda = "black"
cor_do_preenchimento = ""

root = Tk()
root.title('Drawable App')
frame = Frame(root)

# Widgets arranjados com Layout grid dentro de frame
paddings = {'padx': 5, 'pady': 5}

# label
label = ttk.Label(frame, text='Escolha a ferramenta de desenho:')
label.grid(column=0, row=0, sticky=W, **paddings)

# label para cores
cores = ttk.Label(frame, text='Escolha as cores do desenho:')
cores.grid(column=0, row=1, sticky=W, **paddings)

# option menu
tipo_figura_var = StringVar(root)  # Guarda o tipo de figura selecionado no option menu

option_menu = ttk.OptionMenu(frame, tipo_figura_var,
                             'Linha', 'Linha', 'Rabisco', 'Retangulo', 'Oval', 'Circulo')
option_menu.grid(column=1, row=0, sticky=W, **paddings)

# frame para as cores
frame_cores = Frame(frame)
frame_cores.grid(column=1, row=1, sticky=W)

# botao de cor da borda
botao_cor_borda = Button(frame_cores, text="Cor da borda", command=escolher_cor_da_borda)
botao_cor_borda.pack(side="left", padx=0, pady=0)

# indicador da cor da borda
indicador_borda = Canvas(frame_cores, width=20, height=10, bg="black", highlightthickness=1, highlightbackground="gray")
indicador_borda.pack(side="left", padx=5, pady=0)

# botao de cor do preenchimento
botao_cor_preenchimento = Button(frame_cores, text="Cor do preenchimento", command=escolher_cor_do_preenchimento)
botao_cor_preenchimento.pack(side="left", padx=0, pady=0)

# indicador da cor do preenchimento
indicador_preenchimento = Canvas(frame_cores, width=20, height=10, bg="black", highlightthickness=1,
                                 highlightbackground="gray")
indicador_preenchimento.pack(side="left", padx=5, pady=0)

# botao para não ter preenchimento
botao_sem_preenchimento = Button(frame_cores, text="Sem preenchimento", command=remover_preenchimento)
botao_sem_preenchimento.pack(side="left", padx=0, pady=0)


# verificação de alteração no valor do menu
def opcao_mudou(*args):
    opcao_selecionada = tipo_figura_var.get()
    if opcao_selecionada == 'Linha' or opcao_selecionada == 'Rabisco':
        botao_cor_preenchimento.config(state="disabled")
        botao_sem_preenchimento.config(state="disabled")
        indicador_preenchimento.config(bg="#D3D3D3")
    else:
        botao_cor_preenchimento.config(state="normal")
        botao_sem_preenchimento.config(state="normal")
        indicador_preenchimento.config(bg=cor_do_preenchimento or "#D3D3D3")


tipo_figura_var.trace_add('write', opcao_mudou)
opcao_mudou()

# Área de desenho
canvas = Canvas(frame, bg='white', width=600, height=600)
canvas.grid(column=0, row=2, columnspan=2, sticky=W, **paddings)

frame.pack()

# eventos de mouse associados ao canvas - com seus callbacks
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

# eventos de teclado para desfazer/refazer
canvas.bind('<Control-z>', desfazer)
canvas.bind('<Control-y>', refazer)

# focar no canvas para capturar eventos de teclado
canvas.focus_set()

root.mainloop()

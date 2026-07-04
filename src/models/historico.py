class Historico:

    def __init__(self):
        self.figuras = []
        self.figuras_desfeitas = []

    def adicionar(self, figura):
        self.figuras.append(figura)
        self.figuras_desfeitas.clear()

    def desfazer(self):
        if self.figuras:
            figura = self.figuras.pop()
            self.figuras_desfeitas.append(figura)

    def refazer(self):
        if self.figuras_desfeitas:
            figura = self.figuras_desfeitas.pop()
            self.figuras.append(figura)

    def limpar(self):
        self.figuras.clear()
        self.figuras_desfeitas.clear()

    def get_figuras(self):
        return self.figuras
    
    def get_figuras_desfeitas(self):
        return self.figuras_desfeitas
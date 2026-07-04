class Historico:

    def __init__(self):
        self._figuras = []
        self._figuras_desfeitas = []

    @property
    def figuras(self):
        return self._figuras

    @property
    def figuras_desfeitas(self):
        return self._figuras_desfeitas

    def adicionar(self, figura):
        self._figuras.append(figura)
        self._figuras_desfeitas.clear()

    def desfazer(self):
        if self._figuras:
            figura = self._figuras.pop()
            self._figuras_desfeitas.append(figura)

    def refazer(self):
        if self._figuras_desfeitas:
            figura = self._figuras_desfeitas.pop()
            self._figuras.append(figura)

    def limpar(self):
        self._figuras.clear()
        self._figuras_desfeitas.clear()

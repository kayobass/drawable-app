from abc import ABC, abstractmethod


# Criação da classe Figura
class Figura(ABC):
    def __init__(self, values, cor_borda, cor_preenchimento, espessura):
        self.values = values
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
        self.espessura = espessura

    @abstractmethod
    def desenhar(self, canvas):
        pass

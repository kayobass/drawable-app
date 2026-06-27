from abc import ABC, abstractmethod

# Criação da classe Figura
class Figura(ABC):
    def __init__(self, values, cor_borda, cor_preenchimento):
        self.values = values
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento

    @abstractmethod    
    def desenhar(self, canvas):
        pass
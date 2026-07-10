from abc import ABC, abstractmethod


# Criação da classe Figura
class Figura(ABC):
    def __init__(self, values, cor_borda, cor_preenchimento, espessura):
        self.values = values
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento
        self.espessura = espessura
        
    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"
    
    def __eq__(self, other):
        if not isinstance(other, Figura):
            return False
        return (
                self.values == other.values and 
                self.cor_da_borda == other.cor_da_borda and 
                self.cor_do_preenchimento == other.cor_do_preenchimento and 
                self.espessura == other.espessura
                )

    @abstractmethod
    def desenhar(self, canvas):
        pass

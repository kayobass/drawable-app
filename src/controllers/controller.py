from models.figuras import *

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
        
    @classmethod
    def figuras_disponiveis(cls):
        return list(cls.MAPA_FIGURAS.keys())
        
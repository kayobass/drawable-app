from views.view import DrawableView
from controllers.controller import DrawableController
from models.historico import Historico

def main():
    figuras = DrawableController.figuras_disponiveis()
    view = DrawableView(figuras)
    historico = Historico()
    controller = DrawableController(view, historico)
    view.mainloop()

if __name__ == "__main__":
    main()
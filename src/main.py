from controllers.controller import DrawableController
from models.historico import Historico
from views.view import DrawableView


def main():
    view = DrawableView(DrawableController.figuras_disponiveis())
    historico = Historico()

    DrawableController(view, historico)

    view.mainloop()


if __name__ == "__main__":
    main()

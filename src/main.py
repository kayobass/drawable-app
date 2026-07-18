"""
Módulo principal do sistema de desenho.

Inicializa os componentes da aplicação no padrão MVC.

:author: Matheuz Rozendo, Kayo Araujo
:version: OO.MVC.1
:since: OO.1
"""

from controllers.controller import DrawableController
from models.historico import Historico
from views.view import DrawableView


def main():
    """
    Inicializa e executa o sistema de desenho.

    Cria a visão, o histórico, o controlador e inicia o loop principal da interface gráfica.

    :return: None
    :see: DrawableController, DrawableView, Historico
    """
    view = DrawableView(DrawableController.figuras_disponiveis())
    historico = Historico()

    DrawableController(view, historico)

    view.mainloop()


if __name__ == "__main__":
    main()

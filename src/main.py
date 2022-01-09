import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parents[1]))

from src.presenter.presenter import Presenter
from src.presenter.handler import Handler
from src.views.view import InterFace


def main():
    interface = InterFace()
    presenter = Presenter(window=interface.window)
    handler = Handler(presenter)

    while True:
        event, values = interface.window.read()
        handler.handle(event, values)

        if event is None:
            break

    interface.close()


if __name__ == '__main__':
    main()

def main():
    from presenter.presenter import Presenter
    from presenter.handler import Handler
    from views.view import InterFace

    interface = InterFace()
    interface.show_window()
    presenter = Presenter(window=interface.window)
    handler = Handler(presenter)

    while True:
        event, values = interface.window.read()
        handler.handle(event, values)

        if event is None:
            break

    interface.close_window()


if __name__ == '__main__':
    main()

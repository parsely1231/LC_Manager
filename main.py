def main():
    from presenter.presenter import Presenter
    from views.view import InterFace

    interface = InterFace()
    interface.show_window()
    presenter = Presenter(window=interface.window)

    while True:
        event, values = interface.window.read()
        presenter.check_event(event, values)

        if event in ('Exit', 'Quit', None):
            break

    interface.close_window()


if __name__ == '__main__':
    main()

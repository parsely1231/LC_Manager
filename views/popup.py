import PySimpleGUI as sg


class NamePeakPopup:
    def __init__(self, rrt_list):
        cols = [[sg.Text('RRT', size=(5, 1)), sg.Text('Name', size=(15, 1))]] + \
              [[sg.Text(str(rrt), size=(5, 1)), sg.Input(size=(15, 1))] for rrt in rrt_list]

        self.layout = [[sg.Column(cols,scrollable=True , vertical_scroll_only=True, size=(200, 400))],
                       [sg.OK(), sg.Cancel()]]
        self.window = sg.Window(title='Name Peaks', layout=self.layout)
        self.rrt_list = rrt_list
        self.rrt_to_name = {}

    def get_rrt_to_name(self):
        while True:
            event, values = self.window.read()

            if event in ('Exit', 'Quit', 'Cancel', None):
                break

            elif event == 'OK':
                for rrt, name in zip(self.rrt_list, values.values()):
                    if not name:
                        name = None
                    self.rrt_to_name[rrt] = name
                break

        self.window.close()
        return self.rrt_to_name

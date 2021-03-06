import PySimpleGUI as sg

from src.views.style import *


class InterFace:
    def __init__(self):
        self.input_frame = [sg.Frame('Input', font='Any 15', layout=[

                    [sg.Text('Input Text File(Original Format)  or  ASCII Files', **input_text_style)],
                    [sg.Button('Input Text', **input_button_style)],
                    [sg.Button('Input ASCII', **input_ascii_button_style)]

                    ])]

        self.preview_frame = [sg.Frame('Preview', font='Any 15', layout=[

                    [sg.Listbox(**list_box_style), sg.Table(**table_style)]

                    ])]

        self.edit_frame = [sg.Frame('Edit', font='Any 15', layout=[

                    [sg.Button('Calc RRT', **calc_rrt_btn_style),
                     sg.Button('Set Peak Name', **peak_name_btn_style),
                     sg.Button('Set Exclude', **exclude_btn_style)]

                    ])]

        self.output_frame = [sg.Frame('Output', font='Any 15', layout=[

                    [sg.Button('Export Excel File', **export_btn_style)]

                    ])]

        self.layout = [self.input_frame,
                       self.preview_frame,
                       self.edit_frame,
                       self.output_frame]

        self.window = sg.Window(title='LC Data Manager', layout=self.layout, **window_style)

    def close(self):
        self.window.close()

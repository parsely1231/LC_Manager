import PySimpleGUI as sg
import typing


from views.style import *


class InterFace:

    def __init__(self):
        self.window: typing.Optional[sg.Window] = None

        self.input_frame = [sg.Frame('Input', font='Any 15', layout=[

                    [sg.Text('Source Text File', **input_text_style)],
                    [sg.Input(**file_path_entry_style), sg.FileBrowse('Select File', **file_browse_style)],
                    [sg.Button('Input Data', **input_button_style)]

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

    def show_window(self):
        self.window = sg.Window(title='LC Data Manager',layout=self.layout , **window_style)

    def close_window(self):
        self.window.close()

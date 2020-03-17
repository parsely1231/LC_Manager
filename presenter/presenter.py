import PySimpleGUI as sg

from models.hplc_data import ExperimentalData
from models.excel import ExcelModel
from views.popup import NamePeakPopup, ExcludePopup


class Presenter:
    def __init__(self, window: sg.Window):
        self.window = window
        self.exp = ExperimentalData()

    # ------------------for Model-------------------
    def install_text(self, file_path):
        self.exp.install_text(file_path)

    def install_ascii(self, ascii_files):
        self.exp.install_ascii(ascii_files)

    def get_new_table(self, sample_name):
        return self.exp.tables[sample_name]

    def calc_rrt(self, base_rt):
        self.exp.set_base_rt(base_rt)
        self.exp.calc_rrt_in_exp()

    def set_excluded(self, excluded: set):
        self.exp.set_excluded(excluded)
        self.exp.calc_edited_area_ratio_in_exp()

    def set_peak_name(self, rrt_to_name: dict):
        self.exp.set_imp_name_in_exp(rrt_to_name)

    def create_excel(self, file_path):
        excel = ExcelModel()
        excel.to_xlsx(self.exp, file_path)

    # ------------------for View-------------------
    def update_table(self):
        if self.exp.tables:
            self.window['-TABLE-'].update(values=self.exp.tables[self.exp.sample_name_list[0]].detail())

    def input_data_event(self, file_path):
        if file_path[-4:] == '.txt':
            self.install_text(file_path)
            self.window['-SampleList-'].update(values=self.exp.sample_name_list)
            sg.popup('Input has completed')
            self.update_table()
        else:
            sg.popup('#### Error ####\nSelect **TEXT** file')

    def input_ascii_event(self, ascii_files):
        if not ascii_files:
            return
        ascii_files = ascii_files.split(';')
        for file_path in ascii_files:
            if file_path[-4:] != '.txt':
                sg.popup('#### Error ####\nSelect **TEXT** files')
                return
        self.install_ascii(ascii_files)

    def sample_name_check_event(self, sample_names):
        if not sample_names:
            return
        sample_name = sample_names[0]
        new_table = self.get_new_table(sample_name)
        self.window['-TABLE-'].update(values=new_table.detail())

    def calc_rrt_event(self, base_rt):
        if base_rt is None:
            return
        try:
            float(base_rt)
        except ValueError:
            sg.popup('#### Error ####\nOnly numerical')
            return

        base_rt = float(base_rt)
        self.calc_rrt(base_rt)
        sg.popup('Calculation has completed')
        self.update_table()

    def excluded_event(self, excluded):
        self.set_excluded(excluded)
        sg.popup('Excluding has completed')
        self.update_table()

    def peak_name_event(self, rrt_to_name):
        self.set_peak_name(rrt_to_name)
        sg.popup('Name Peaks has completed')
        self.update_table()

    def save_event(self, file_path):
        self.create_excel(file_path)
        sg.popup('Export has completed')

    #  ------------------event check--------------------
    def check_event(self, event, value):
        if event == '-InputData-':
            file_path = value['-SourceFile-']
            self.input_data_event(file_path)

        elif event == '-InputASCII-':
            ascii_files = sg.popup_get_file('Select ASCII files',
                                            file_types=(("Text File", "*.txt"),), multiple_files=True)
            self.input_ascii_event(ascii_files)

        elif event == '-SampleList-':
            sample_names = self.window['-SampleList-'].get()
            self.sample_name_check_event(sample_names)

        elif event == '-CalcRRT-':
            base_rt = sg.popup_get_text('Input Base RT')
            self.calc_rrt_event(base_rt)

        elif event == '-PeakName-':
            rrt_list = sorted(list(self.exp.rrt_set))
            popup = NamePeakPopup(rrt_list)
            rrt_to_name = popup.get_rrt_to_name()
            print(rrt_to_name)
            if rrt_to_name:
                self.peak_name_event(rrt_to_name)
            del popup

        elif event == '-Exclude-':
            name_list = self.exp.imp_name_list
            popup = ExcludePopup(name_list)
            excluded = popup.get_excluded()
            if excluded:
                self.excluded_event(excluded)
            del popup

        elif event == '-Output-':
            file_path = sg.popup_get_file('Create Excel', file_types=(("Excel File", "*.xlsx"),),
                                          default_extension='default.xlsx', save_as=True)
            if file_path[-4:] != '.xlsx':
                file_path = file_path + '.xlsx'
            self.save_event(file_path)

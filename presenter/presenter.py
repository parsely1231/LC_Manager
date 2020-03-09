import PySimpleGUI as sg

from models.hplc_data import ExperimentalData
from models.excel import ExcelModel


class Presenter:
    def __init__(self, window: sg.Window):
        self.window = window
        self.exp = ExperimentalData()

    # ------------------for Model-------------------
    def install_text(self, file_path):
        self.exp.install_text(file_path)

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
    def input_data_event(self, file_path):
        if file_path[-4:] == '.txt':
            self.install_text(file_path)
            self.window['-SampleList-'].update(values=self.exp.sample_name_list)
            sample = self.exp.sample_name_list[0]
            table = self.exp.tables[sample]
            self.window['-TABLE-'].update(values=table.detail())
            sg.popup('Input has completed')
        else:
            sg.popup('#### Error ####\nSelect **TEXT** file')

    def sample_name_check_event(self):
        if not self.window['-SampleList-'].get():
            return
        sample_name = self.window['-SampleList-'].get()[0]
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
        self.window['-TABLE-'].update(values=self.exp.tables[self.exp.sample_name_list[0]].detail())
        sg.popup('Calculation has completed')

    def excluded_event(self, excluded):
        self.set_excluded(excluded)

    def peak_name_event(self, rrt_to_name):
        self.set_peak_name(rrt_to_name)

    def save_event(self, file_path):
        self.create_excel(file_path)
        sg.popup('Export has completed')

    #  ------------------event check--------------------
    def check_event(self, event, value):
        """TODO MUST
        peakname function & exclude function"""
        if event == '-InputData-':
            file_path = value['-SourceFile-']
            self.input_data_event(file_path)

        elif event == '-SampleList-':
            self.sample_name_check_event()

        elif event == '-CalcRRT-':
            base_rt = sg.popup_get_text('Input Base RT')
            self.calc_rrt_event(base_rt)

        elif event == '-PeakName-':
            pass

        elif event == '-Exclude-':
            pass

        elif event == '-Output-':
            file_path = sg.popup_get_file('Create Excel', file_types=(("Excel File", "*.xlsx"),),
                                          default_extension='default.xlsx', save_as=True)
            if file_path[-4:] != '.xlsx':
                file_path = file_path + '.xlsx'
            self.save_event(file_path)

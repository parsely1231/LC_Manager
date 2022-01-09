import PySimpleGUI as sg

from src.models.hplc_data import ExperimentalData
from src.models.excel import ExcelModel
from src.views.popup import NamePeakPopup, ExcludePopup
from src.presenter.validator import Validator


class Presenter:
    def __init__(self, window: sg.Window):
        self.window = window
        self.exp = ExperimentalData()
        self.validator = Validator

    # ------------------to Model-------------------
    def install_text(self, file_path):
        self.exp.install_text(file_path)

    def install_ascii(self, ascii_files):
        self.exp.install_ascii(ascii_files)

    def calc_rrt(self, base_rt):
        self.exp.set_base_rt(base_rt)
        self.exp.calc_rrt_in_exp()

    def set_excluded(self, excluded: set):
        self.exp.set_excluded(excluded)
        self.exp.calc_edited_area_ratio_in_exp()

    def set_peak_name(self, rrt_to_name: dict):
        self.exp.set_imp_name_in_exp(rrt_to_name)

    # -----------------from Model-------------------
    def get_new_table(self, sample_name):
        return self.exp.tables[sample_name]

    def create_excel(self, file_path):
        excel = ExcelModel()
        excel.to_xlsx(self.exp, file_path)

    # ------------------to View---------------------
    def update_table(self, table_name):
        new_table = self.get_new_table(table_name)
        self.window['-TABLE-'].update(values=new_table.detail())

    def update_listbox(self):
        self.window['-SampleList-'].update(values=self.exp.sample_name_list)

    def enable_button(self, key):
        self.window[key].update(disabled=False)

    @staticmethod
    def show_error(message):
        sg.popup_error(message)

    @staticmethod
    def show_success(message):
        sg.popup(message)

    # -----------------from View--------------------
    def receive_text_file_path(self):
        file_path = sg.popup_get_file('Select "Original Format" Text file', file_types=(("Text File", "*.txt"),))

        if not file_path:
            return False
        if not self.validator.text_file_validate(file_path):
            self.show_error('#### Error ####\nSelect **TEXT** file(.txt)')
            return False

        return file_path

    def receive_ascii_file_paths(self):
        ascii_files: str = sg.popup_get_file('Select ASCII files', file_types=(("Text File", "*.txt"),), multiple_files=True)

        if not ascii_files:
            return False
        if not self.validator.text_files_validate(ascii_files):
            self.show_error('#### Error ####\nSelect **TEXT** files')
            return False

        return ascii_files.split(";")

    def receive_base_rt(self):
        base_rt = sg.popup_get_text('Input Base RT')

        if not base_rt:
            return False
        if not self.validator.base_rt_validate(base_rt):
            self.show_error('#### Error ####\nOnly numerical  and  not 0')
            return False

        return float(base_rt)

    def receive_rrt_to_name(self):
        rrt_list = sorted(list(self.exp.rrt_set))
        popup = NamePeakPopup(rrt_list)
        rrt_to_name = popup.get_rrt_to_name()
        del popup
        return rrt_to_name

    def receive_excluded(self):
        name_list = self.exp.imp_name_list
        popup = ExcludePopup(name_list)
        excluded = popup.get_excluded()
        del popup
        return excluded

    def receive_xlsx_path(self):
        file_path = sg.popup_get_file('Create Excel', file_types=(("Excel File", "*.xlsx"),),
                                      default_extension='default.xlsx', save_as=True)
        if not file_path:
            return False
        validate_result = self.validator.xlsx_file_validate(file_path)
        if not validate_result:
            self.show_error('#### Error ####\nFilename needs **.xlsx**')
            return False

        elif validate_result == 'add xlsx':
            file_path = file_path + '.xlsx'

        return file_path

    # ---------------- Event process----------------
    def input_text_event(self, _):
        file_path = self.receive_text_file_path()
        if not file_path:
            return
        self.install_text(file_path)
        self.update_listbox()
        first_sample = self.exp.sample_name_list[0]
        self.update_table(first_sample)
        self.enable_button('-Output-')
        self.show_success('Input has completed')

    def input_ascii_event(self, _):
        ascii_files = self.receive_ascii_file_paths()
        if not ascii_files:
            return
        self.install_ascii(ascii_files)
        self.update_listbox()
        first_sample = self.exp.sample_name_list[0]
        self.update_table(first_sample)
        self.enable_button('-Output-')
        self.show_success('Input has completed')

    def sample_name_check_event(self, values):
        sample_names = values['-SampleList-']
        if not sample_names:
            return

        checked_name = sample_names[0]
        self.update_table(checked_name)

    def calc_rrt_event(self, _):
        base_rt = self.receive_base_rt()
        if not base_rt:
            return
        self.calc_rrt(base_rt)
        first_sample = self.exp.sample_name_list[0]
        self.update_table(first_sample)
        self.show_success('Calculation has completed')

    def peak_name_event(self, _):
        rrt_to_name = self.receive_rrt_to_name()
        if not rrt_to_name:
            return

        self.set_peak_name(rrt_to_name)
        first_sample = self.exp.sample_name_list[0]
        self.update_table(first_sample)
        self.enable_button('-Exclude-')
        self.show_success('Name Peaks has completed')

    def excluded_event(self, _):
        excluded = self.receive_excluded()
        if not excluded:
            return

        self.set_excluded(excluded)
        first_sample = self.exp.sample_name_list[0]
        self.update_table(first_sample)
        self.show_success('Excluding has completed')

    def save_event(self, _):
        file_path = self.receive_xlsx_path()
        if not file_path:
            return

        self.create_excel(file_path)
        self.show_success('Export has completed')

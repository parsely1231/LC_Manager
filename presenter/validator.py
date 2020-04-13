import re


class Validator:
    @classmethod
    def text_file_validate(cls, file_path):
        if re.search('.txt$', file_path):
            return True
        else:
            return False

    @classmethod
    def text_files_validate(cls, file_paths):
        file_paths = file_paths.split(';')
        for file_path in file_paths:
            if not cls.text_file_validate(file_path):
                return False

        return True

    @classmethod
    def xlsx_file_validate(cls, file_path):
        if '.' in file_path:
            if not re.search('.xlsx$', file_path):  # 別の拡張子のとき
                return False
        else:  # 拡張子がないとき
            return 'add xlsx'

    @classmethod
    def base_rt_validate(cls, base_rt):
        if base_rt is None:
            return False

        try:
            float(base_rt)
        except ValueError:
            return False

        if float(base_rt) == 0:
            return False

        return True

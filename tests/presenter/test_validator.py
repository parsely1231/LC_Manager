from presenter.validator import Validator


class TestValidator:
    def test_text_file_validate(self):
        assert Validator.text_file_validate('test.txt') == True

    def test_text_file_validate_ng(self):
        assert Validator.text_file_validate('test.txxt') == False

    def test_text_files_validate(self):
        ok_files = 'abc.txt;xyz.txt;1020.txt'
        assert Validator.text_files_validate(ok_files) == True

    def test_text_files_validate_ng(self):
        ng_files = 'abc.txt;xyz.txt;1020txt'
        assert Validator.text_files_validate(ng_files) == False

    def test_xlsx_file_validate(self):
        assert Validator.xlsx_file_validate('test.xlsx') == True

    def test_xlsx_file_validate_other_type(self):
        assert Validator.xlsx_file_validate('test.txt') == False

    def test_xlsx_file_validate_no_extension(self):
        assert Validator.xlsx_file_validate('test') == 'add xlsx'

    def test_base_rt_validate(self):
        assert Validator.base_rt_validate('3.33') == True

    def test_base_rt_validate_no_numerical(self):
        assert Validator.base_rt_validate('sss') == False

    def test_base_rt_validate_zero(self):
        assert Validator.base_rt_validate('0') == False

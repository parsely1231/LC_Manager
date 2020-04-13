from decimal import Decimal

from models.excel import ExcelModel
from models.hplc_data import ExperimentalData


class TestExcelModel:
    def test_to_xlsx(self):
        exp = ExperimentalData()
        test_file = '../../sample_file/sample.txt'
        exp.install_text(test_file)
        rro_to_name = {Decimal('1.22'): 'blank', Decimal('2.22'): 'solvent'}
        exp.set_imp_name_in_exp(rro_to_name)
        exp.set_excluded({'blank', 'solvent'})
        exp.calc_edited_area_ratio_in_exp()
        excel = ExcelModel()
        excel.to_xlsx(exp, './test.xlsx')

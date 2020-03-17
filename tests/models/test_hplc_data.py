from models.hplc_data import ImpurityData, DataTable, ExperimentalData


from decimal import Decimal


class TestImpData:
    test_rt = 5
    test_area = 100000
    test_area_ratio = 99.99

    @classmethod
    def setup_class(cls):
        cls.data = ImpurityData(cls.test_rt, cls.test_area, cls.test_area_ratio)

    @classmethod
    def teardown_class(cls):
        del cls.data

    def setup_method(self, method):
        print(f'method = {method.__name__}: test start')

    def teardown_method(self, method):
        print(f'method = {method.__name__}: test finished')

    def test_detail(self):
        assert self.data.detail() == [None, self.test_rt, None, self.test_area, self.test_area_ratio, None]

    def test_set_imp_rrt(self):
        self.data.set_imp_rrt(10.0)
        assert self.data.rrt == Decimal(0.5)

    def test_set_imp_name(self):
        self.data.set_imp_name({'0.4': 'test'})
        assert self.data.name is None
        self.data.set_imp_name({Decimal(0.5): 'test'})
        assert self.data.name == 'test'

    def test_set_edited_area_ratio(self):
        self.data.set_edited_area_ratio(200000)
        assert self.data.edited_area_ratio == Decimal(50.0)


class TestDataTable:
    """TODO """


class TestExperimentalData:
    """TODO"""

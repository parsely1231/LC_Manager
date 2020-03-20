from models.hplc_data import ImpurityData, DataTable, ExperimentalData


from decimal import Decimal


class TestImpData:
    test_rt = 5
    test_area = 100000
    test_area_ratio = 99.99

    @classmethod
    def setup_class(cls):
        print(f'Model: ImpData Class test start')
        cls.data = ImpurityData(cls.test_rt, cls.test_area, cls.test_area_ratio)

    @classmethod
    def teardown_class(cls):
        del cls.data

    def setup_method(self, method):
        print(f'method = {method.__name__}')

    def teardown_method(self):
        print('finished')

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
    @classmethod
    def setup_class(cls):
        print(f'Model: DataTable Class test start')
        cls.table = DataTable('test_table')
        cls.table.add_imp_data(ImpurityData(5.0, 10000, 10.0))
        cls.table.add_imp_data(ImpurityData(10.0, 90000, 90.0))

    @classmethod
    def teardown_class(cls):
        del cls.table

    def setup_method(self, method):
        print(f'method = {method.__name__}')

    def teardown_method(self):
        print('finished')

    def test_detail(self):
        details = self.table.detail()
        second = details.pop()
        first = details.pop()
        assert first == [None, 5.0, None, 10000, 10.0, None]
        assert second == [None, 10.0, None, 90000, 90.0, None]

    def test_set_std_rt(self):
        self.table.set_std_rt(7.0)
        assert self.table.std_rt == 7.0
        self.table.set_std_rt(5.1)
        assert self.table.std_rt == 5.0

    def test_calc_rrt_in_table(self):
        self.table.calc_rrt_in_table()
        assert self.table.rrt_set == {Decimal(1.0), Decimal(2.0)}


class TestExperimentalData:
    """TODO"""

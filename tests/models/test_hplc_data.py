from src.models.hplc_data import ImpurityData, DataTable, ExperimentalData


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
    TEST_TEXT = 'sample_file/sample.txt'
    TEST_ASCII = 'sample_file/ASCIIsample2.txt'
    @classmethod
    def setup_class(cls):
        print(f'Model: ExperimentalData Class test Start')

    @classmethod
    def teardown_class(cls):
        print(f'Model: ExperimentalData Class test Finish')

    def setup_method(self, method):
        self.exp = ExperimentalData()

    def teardown_method(self):
        del self.exp

    def test_install_text(self):
        test_file = self.TEST_TEXT
        test_data = [[None, 1.222, Decimal('1.22'), 10000, 10.0, Decimal('10.00')],
                     [None, 2.222, Decimal('2.22'), 10000, 10.0, Decimal('10.00')],
                     [None, 9.123, Decimal('9.12'), 80000, 80.0, Decimal('80.00')]]
        self.exp.install_text(test_file)
        assert self.exp.sample_name_list == ['#sample1', '#sample2', '#sample3']
        assert self.exp.tables['#sample1'].detail() == test_data

    def test_ascii_to_table(self):
        test_file = self.TEST_ASCII
        test_data = [[None, 1.84, None, 1384, 0.0003338428618052167, None],
                     [None, 2.101, None, 1295, 0.00031237464309086385, None],
                     [None, 2.213, None, 1621, 0.00039101103972995395, None],
                     [None, 3.526, None, 13512, 0.0032593097895318554, None],
                     [None, 5.005, None, 120641, 0.029100532291216147, None],
                     [None, 19.033, None, 3823843, 0.9223718859926627, None],
                     [None, 24.767, None, 10237, 0.002469327584031794, None],
                     [None, 29.027, None, 173130, 0.041761715797931476, None]]
        test_name = 'ZZZZZZZ'
        self.exp.ascii_to_table(test_file)
        assert self.exp.tables['ZZZZZZZ'].detail() == test_data

    def test_set_imp_name_in_exp(self):
        test_data = [['blank', 1.222, Decimal('1.22'), 10000, 10.0, Decimal('10.00')],
                     ['solvent', 2.222, Decimal('2.22'), 10000, 10.0, Decimal('10.00')],
                     [None, 9.123, Decimal('9.12'), 80000, 80.0, Decimal('80.00')]]
        rro_to_name = {Decimal('1.22'): 'blank', Decimal('2.22'): 'solvent'}
        test_file = self.TEST_TEXT

        self.exp.install_text(test_file)
        self.exp.set_imp_name_in_exp(rro_to_name)
        assert self.exp.tables['#sample1'].detail() == test_data

    def test_calc_edited_area_ratio_in_exp(self):
        test_data = [['blank', 1.222, Decimal('1.22'), 10000, 10.0, None],
                     ['solvent', 2.222, Decimal('2.22'), 10000, 10.0, None],
                     [None, 9.123, Decimal('9.12'), 80000, 80.0, Decimal('100.00')]]
        rro_to_name = {Decimal('1.22'): 'blank', Decimal('2.22'): 'solvent'}
        test_file = self.TEST_TEXT

        self.exp.install_text(test_file)
        self.exp.set_imp_name_in_exp(rro_to_name)
        self.exp.set_excluded({'blank', 'solvent'})
        self.exp.calc_edited_area_ratio_in_exp()
        assert self.exp.tables['#sample1'].detail() == test_data

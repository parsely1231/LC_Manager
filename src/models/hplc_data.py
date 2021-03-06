from typing import List, Dict, Optional
from decimal import Decimal, ROUND_HALF_UP


class ImpurityData:
    """不純物一つ分のデータ"""

    def __init__(self, rt, area, area_ratio):
        self.rt = rt
        self.area = area
        self.area_ratio = area_ratio
        self.edited_area_ratio = None
        self.rrt = None
        self.name = None

    def detail(self):
        return [self.name, self.rt, self.rrt, self.area, self.area_ratio, self.edited_area_ratio]

    def set_imp_rrt(self, std_rt):
        self.rrt = Decimal(str(self.rt/std_rt)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def set_imp_name(self, rrt_to_name: dict):
        if self.rrt not in rrt_to_name:
            return
        name = rrt_to_name[self.rrt]
        self.name = name

    def set_edited_area_ratio(self, edited_total_area):
        self.edited_area_ratio = Decimal(str(100*self.area / edited_total_area)).quantize(Decimal('00.00'),
                                                                                          rounding=ROUND_HALF_UP)


class DataTable:
    """HPLC分析一回分のデータ(ImpurityDataのリスト)"""
    imp_list: List[ImpurityData]

    def __init__(self, name):
        self.name = name
        self.imp_list = []
        self.std_rt = None
        self.rrt_set = set()
        self.total_area = None
        self.edited_total_area = None

    def detail(self):
        return [imp.detail() for imp in self.imp_list]

    def add_imp_data(self, imp: ImpurityData):
        self.imp_list.append(imp)

    def set_std_rt(self, base_rt):
        """tableのstd_rtを設定する.
        std_rtはtable内の各imp_dataからbase_rt±0.2以内のrtを探して設定する.
        条件にあうrtがない場合はbase_rtをそのまま設定"""
        candidates = [imp.rt for imp in self.imp_list if base_rt - 0.2 <= imp.rt <= base_rt + 0.2]
        if candidates:
            self.std_rt = min(candidates)
        else:
            self.std_rt = base_rt

    def calc_rrt_in_table(self):
        """table内の各dataについて、table.std_rtをもとにrrtを計算する"""
        self.rrt_set = set()
        for imp in self.imp_list:
            imp.set_imp_rrt(self.std_rt)
            while imp.rrt in self.rrt_set:
                imp.rrt += Decimal('0.001')
            self.rrt_set.add(imp.rrt)

    def set_total_area(self):
        total_area = sum([imp.area for imp in self.imp_list])
        self.total_area = total_area

    def set_edited_total_area(self, excluded):
        edited_total_area = sum([imp.area for imp in self.imp_list if imp.name not in excluded])
        self.edited_total_area = edited_total_area

    def calc_edited_area_ratio_in_table(self, excluded):
        for imp in self.imp_list:
            if imp.name in excluded:
                imp.edited_area_ratio = None
            else:
                imp.set_edited_area_ratio(self.edited_total_area)

    def set_imp_name_in_table(self, rrt_to_name: dict):
        for imp in self.imp_list:
            imp.set_imp_name(rrt_to_name)


class ExperimentalData:
    """実験で得られた全てのHPLC分析データ(DataTableのdict)"""
    tables: Dict[str, DataTable]

    def __init__(self):
        self.sample_name_list = []
        self.tables = {}
        self.rrt_set = set()
        self.imp_excluded = set()
        self.base_rt = 1
        self.imp_name_list = []

    # ---------テキストの読み込み-----------
    def install_text(self, text_file_path):
        """テキストファイルを読み込んで実験データを構築する"""

        def is_sample_name_line(text_line):
            """テキストファイルの様式ルールとして、サンプルの名前であることを「#」で明示する"""
            return text_line[0] == '#'

        def is_imp_data_line(text_line):
            """テキストファイルの様式ルールとして、先頭に数字がくる行は不純物データとする"""
            return text_line[0].isdecimal()

        table: Optional[DataTable] = None

        with open(text_file_path, 'r') as file_open:
            for line in file_open:

                if is_sample_name_line(line):
                    sample_name = line.replace('\n', '')
                    table = DataTable(sample_name)

                elif is_imp_data_line(line):
                    rt, area, area_ratio, *others = line.split()
                    imp_data = ImpurityData(float(rt), int(area), float(area_ratio))
                    table.add_imp_data(imp_data)

                else:  # 何もない行は分析データごとの切れ目なので、tableをexpに保管したのち初期化する
                    if table is not None:
                        table.set_total_area()
                        self.add_table(table)
                        table = None

        if table is not None:
            table.set_total_area()
            self.add_table(table)
        self.calc_rrt_in_exp()
        self.calc_edited_area_ratio_in_exp()

    def install_ascii(self, ascii_files):
        for asc_file in ascii_files:
            self.ascii_to_table(asc_file)
        self.calc_rrt_in_exp()
        self.calc_edited_area_ratio_in_exp()

    def ascii_to_table(self, ascii_file):
        def is_sample_name_line(text_line):
            """ASCIIファイルの様式として、サンプル名の行はSampleNameで始まる"""
            splitted_line = text_line.split()
            return splitted_line[0] == 'Sample' and splitted_line[1] == 'Name'

        def is_imp_data_line(text_line):
            """ASCIIファイルの様式として、先頭に数字がくる行は不純物データである"""
            return text_line[0].isdecimal()

        def is_finish_line(text_line):
            return text_line == '[Compound Results(PDA)]'

        table: Optional[DataTable] = None

        with open(ascii_file, 'r') as file_open:
            for line in file_open:
                line = line.rstrip('\n')
                if not line:
                    continue

                elif is_sample_name_line(line):
                    sample_name = line.split()[2]
                    table = DataTable(sample_name)

                elif is_imp_data_line(line):
                    data = line.split()
                    rt, area = data[1], data[4]
                    imp_data = ImpurityData(float(rt), int(area), None)
                    table.add_imp_data(imp_data)

                elif is_finish_line(line):
                    break

        table.set_total_area()
        for imp_data in table.imp_list:
            imp_data.area_ratio = imp_data.area / table.total_area

        self.add_table(table)

    def add_table(self, table: DataTable):
        """expにtableを追加する"""
        while table.name in self.tables:
            table.name = table.name + '0'

        self.sample_name_list.append(table.name)
        self.tables[table.name] = table

    # ------------RRT計算処理--------------
    def set_base_rt(self, base_rt):
        self.base_rt = base_rt

    def calc_rrt_in_exp(self):
        self.rrt_set = set()
        for _, table in self.tables.items():
            table.set_std_rt(self.base_rt)
            table.calc_rrt_in_table()
            self.rrt_set.update(table.rrt_set)

    # -----------例外ピーク処理--------------
    def set_excluded(self, excluded: set):
        """expのimp_excludeを設定する"""
        self.imp_excluded = excluded

    def calc_edited_area_ratio_in_exp(self):
        for _, table in self.tables.items():
            table.set_edited_total_area(self.imp_excluded)
            table.calc_edited_area_ratio_in_table(self.imp_excluded)

    # ----------ピーク名付与処理--------------
    def set_imp_name_in_exp(self, rrt_to_name: dict):
        """exp内の全てのimp_dataについて、rrtに対応するnameを設定する"""
        self.imp_name_list = [name for name in rrt_to_name.values() if name is not None]
        for _, table in self.tables.items():
            table.set_imp_name_in_table(rrt_to_name)

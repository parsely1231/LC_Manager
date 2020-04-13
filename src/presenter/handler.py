from src.presenter.presenter import Presenter


class Handler:
    def __init__(self, presenter: Presenter):
        self.presenter = presenter
        self.func_dict = {
            '-InputText-': self.presenter.input_text_event,
            '-InputASCII-': self.presenter.input_ascii_event,
            '-SampleList-': self.presenter.sample_name_check_event,
            '-CalcRRT-': self.presenter.calc_rrt_event,
            '-PeakName-': self.presenter.peak_name_event,
            '-Exclude-': self.presenter.excluded_event,
            '-Output-': self.presenter.save_event
        }

    def handle(self, event_key, values):
        if event_key not in self.func_dict:
            return
        event_func = self.func_dict[event_key]
        event_func(values)

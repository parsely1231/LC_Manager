# -------------Window--------------
window_style = {
    'auto_size_text': False,
    'auto_size_buttons': False,
    'default_element_size': (20, 1),
    'text_justification': 'right',
}

# -----------Input Frame-----------
input_text_style = {
    'font': (None, 12),
    'justification': 'left',
    'size': (40, 1),
}

input_button_style = {
    'size': (15, 1),
    'key': '-InputText-',
}

input_ascii_button_style = {
    'size': (15, 1),
    'key': '-InputASCII-',
}

# -----------Preview Frame-----------
list_box_style = {
    'values': [],
    'font': (None, 12),
    'select_mode': 'LISTBOX_SELECT_MODE_SINGLE',
    'enable_events': True,
    'size': (20, 20),
    'key': '-SampleList-',
}

table_cols = ["Name", "RT", "RRT", "Area", "Area%", "ex-Area%"]
cols_width = [20, 20, 20, 40, 40, 20]
def_data = [['xxxxxx', '0.000', '0.000', '00000000', '00.0', '00.0']]
table_style = {
    'values': def_data,
    'headings': table_cols,
    'max_col_width': 200,
    'def_col_width': cols_width,
    'num_rows': 15,
    'auto_size_columns': True,
    'key': '-TABLE-'
}

# -----------Edit Frame-----------
base_rt_entry_style = {
    'width': 40,
}

calc_rrt_btn_style = {
    'size': (15, 1),
    'key': '-CalcRRT-',
}

peak_name_btn_style = {
    'size': (15, 1),
    'key': '-PeakName-',
}

exclude_btn_style = {
    'size': (15, 1),
    'key': '-Exclude-',
}

# -----------Output Frame-----------
export_btn_style = {
    'button_color': ('white', 'blue'),
    'size': (20, 1),
    'key': '-Output-',
}

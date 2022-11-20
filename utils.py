from collections import namedtuple
from pathlib import Path

LOCAL = '/home/joanna/Dropbox/Projects/anatomy/data/'
REPO = './data/'

def gen_unit_data(unit: str):
    """Generate a named tuple of CSV file names and list of columns to keep, specific to each Unit"""
    path_data = Path(REPO)
    if unit == 'BIOS1168':
        file_describe = 'iap_descriptive_CS0378727_with_age.csv'
        file_exposed = 'BIOS1168_replacement_2019.csv'
        file_control = 'BIOS1168_Results_Sem2_2020_R1.csv'
        keep_exp = ['id',
                    'mse_30_percent', 'ese_prac_30_percent', 'ese_theory_40_percent',
                    'grade', 'age', 'gender', 'atar', 'course_code']
        keep_con = ['id',
                    'mse_40_percent', 'ese_60_percent',
                    'grade', 'age', 'gender', 'atar', 'course_code']

    if unit == 'BIOS5090':
        file_describe = 'iap_descriptive_CS0378727_with_age.csv'
        file_exposed = 'BIOS5090_final_2019.csv'
        file_control = 'BIOS5090_final_2020.csv'
        keep_exp = ['id',
                    'mse_30_percent', 'ese_prac_30_percent', 'ese_theory_35_percent',
                    'grade', 'age', 'gender', 'atar', 'course_code']
        keep_con = ['id',
                    'mse_40_percent', 'ese_55_percent',
                    'grade', 'age', 'gender', 'atar', 'course_code']

    Unit_Info = namedtuple('Unit_Info', 'file_describe file_exposed file_control keep_exp keep_con path_data')
    return Unit_Info(file_describe=file_describe, file_exposed=file_exposed, file_control=file_control, keep_exp=keep_exp, keep_con=keep_con, path_data=path_data)

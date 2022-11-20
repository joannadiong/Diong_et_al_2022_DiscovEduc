import pandas as pd
import proc
import plot
import utils

# ------------------------------------------------------------
# PROCESS AND DE-IDENTIFY DATASET: **COMMENT OUT FOR REPO**
# ------------------------------------------------------------

"""
unit = 'BIOS1168'
semester = 'Semester 2'
proc.clean_and_process_data(unit, semester)

unit = 'BIOS5090'
semester = 'Semester 1'
proc.clean_and_process_data(unit, semester)
"""

# ------------------------------------------------------------
# ANALYSE DE-IDENTIFIED, CLEANED DATA
# ------------------------------------------------------------

unit = 'BIOS1168'
unit_info = utils.gen_unit_data(unit)
df_1168_merged = pd.read_csv(unit_info.path_data / 'proc' / 'bios1168_proc_.csv')
df_1168 = proc.describe_data(df_1168_merged, unit, unit_info.path_data)
proc.analyse_data(df_1168, unit, unit_info.path_data)
plot.plot_independent_groups(unit)

unit = 'BIOS5090'
unit_info = utils.gen_unit_data(unit)
df_5090_merged = pd.read_csv(unit_info.path_data / 'proc' / 'bios5090_proc_.csv')
df_5090 = proc.describe_data(df_5090_merged, unit, unit_info.path_data)
proc.analyse_data(df_5090, unit, unit_info.path_data)
plot.plot_independent_groups(unit)

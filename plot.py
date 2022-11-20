import random
import numpy as np
import pandas as pd
import pliffy as pl

import utils

# For testing plot.py
# unit = 'BIOS1168'

def plot_independent_groups(unit):
    random.seed(123)
    unit_info = utils.gen_unit_data(unit)
    file = '_'.join([unit.lower(), 'clean', '.csv'])

    df = pd.read_csv(unit_info.path_data / 'proc' / file)

    control = df[df['group'] == 0]['ese_100_percent'].values
    # drop missing values. ~: negation operator
    control = control[~np.isnan(control)]
    random.shuffle(control)

    exposed = df[df['group'] == 1]['ese_100_percent'].values
    exposed = exposed[~np.isnan(exposed)]
    random.shuffle(exposed)

    info = pl.PliffyInfoABD(
        data_a=control,
        data_b=exposed,
        measure_units='Mark (%)',
        xtick_labels=pl.ABD(a='Online', b='Face-to-face', diff='Difference'),
        plot_name=unit.lower(),
        save=True,
        width_height_in_inches=(4, 3),
        dpi=600,
        save_type='pdf', # change to svg
        save_path=unit_info.path_data / 'proc'
        )
    pl.plot_abd(info)

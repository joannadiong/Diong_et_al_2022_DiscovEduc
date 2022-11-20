import numpy as np
import pandas as pd
from pathlib import Path
import statsmodels.formula.api as smf

import utils

def clean_and_process_data(unit: str, semester: str):
    """Generate Unit info. Process and merge descriptive and cohort data.
    Clean and describe data. Return cleaned dataframe"""
    unit_info = utils.gen_unit_data(unit)
    df_des, df_exp, df_con = _read_local_and_descriptive_datasets(unit_info.file_describe, unit_info.file_exposed, unit_info.file_control, unit_info.path_data)
    df_exp_merged = _merge_local_and_descriptive_datasets(df_exp, df_des, unit, 2019, semester, unit_info.keep_exp)
    df_con_merged = _merge_local_and_descriptive_datasets(df_con, df_des, unit, 2020, semester, unit_info.keep_con)
    df_merged = _concat_exp_con_df(df_exp_merged, df_con_merged, unit, unit_info.path_data)
    _proc_merge_df(df_merged, unit, unit_info.path_data)


def describe_data(df_merged: pd.DataFrame, unit: str, path_data: Path):
    """Read in de-identified, processed data. Check scores for IC, AF, and FA==0 grades.
    Clean and describe data. Export cleaned data to CSV for R analysis"""
    df = _describe_df(df_merged, unit, path_data)
    return df


def analyse_data(df: pd.DataFrame, unit: str, path_data: Path):
    """Do OLS regression of score on group"""
    md = smf.ols(formula='ese_100_percent ~ group', data=df)

    file = '_'.join([unit.lower(), 'result', '.txt'])
    file = (path_data / 'proc' / file)
    with open(file, 'a') as file:
        file.write('\n\nLinear regression of ESE score on group:\n\n')
        file.write(str(md.fit().summary()))


def _read_local_and_descriptive_datasets(file_describe: str, file_exposed: str, file_control: str, path_data: Path):
    """Read in Unit file names and return separate dataframes of descriptive, exposed and control cohorts"""
    describe = path_data / 'raw' / file_describe
    exposed = path_data / 'raw' / file_exposed  # 2019: face-to-face
    control = path_data / 'raw' / file_control  # 2020: online

    df_des = pd.read_csv(describe)
    df_exp = pd.read_csv(exposed)
    df_con = pd.read_csv(control)

    return df_des, df_exp, df_con


def _merge_local_and_descriptive_datasets(df_local: pd.DataFrame, df_des: pd.DataFrame, unit: str, year: int, semester: str, keepvars: list):
    """Merge the descriptive data with exposed or control cohort. Return a single merged dataframe"""
    df_merged = pd.merge(left=df_local.astype(str),
                         right=df_des[(df_des['uos_code'] == unit) &
                                      (df_des['year'] == year) &
                                      (df_des['sem'] == semester)].astype(str),
                         how='outer',
                         on='sid')
    df_merged['id'] = df_merged.index

    # drop SID, keep desired variables
    df_merged = df_merged[keepvars]

    # drop rows of students who enrolled and withdrew: these do not have a grade for the Unit
    df_merged = df_merged.dropna(axis=0, subset=['grade'])
    if year == 2019:
        df_merged['group'] = 1
    elif year == 2020:
        df_merged['group'] = 0

    return df_merged


def _concat_exp_con_df(df_exp: pd.DataFrame, df_con: pd.DataFrame, unit: str, path_data: Path):
    """Concatenate exposed and control cohorts, return concat dataframe"""
    df_concat = pd.concat([df_exp, df_con], axis=0, ignore_index=True)
    df_concat['uid'] = df_concat.index
    file = '_'.join([unit.lower(), 'init', '.csv'])
    df_concat.to_csv(path_data / 'proc' / file)
    return df_concat


def _proc_merge_df(df: pd.DataFrame, unit: str, path_data: Path):
    """Read in concat dataframe.
    Combine different ESE scores by their proportions, get a 100% value.
    Return processed dataframe and export to CSV"""
    if unit == 'BIOS1168':
        df['ese_100_percent'] = np.nan
        df.loc[df['group'] == 1, 'ese_100_percent'] = (df['ese_prac_30_percent'].astype(float) + df['ese_theory_40_percent'].astype(float)) / 0.7
        df.loc[df['group'] == 0, 'ese_100_percent'] = df['ese_60_percent'].astype(float) / 0.6

    if unit == 'BIOS5090':
        df['ese_100_percent'] = np.nan
        df.loc[df['group'] == 1, 'ese_100_percent'] = (df['ese_prac_30_percent'].astype(float) + df['ese_theory_35_percent'].astype(float)) / 0.65
        df.loc[df['group'] == 0, 'ese_100_percent'] = df['ese_55_percent'].astype(float) / 0.55

    keepvars = ['uid', 'id', 'grade', 'age', 'gender', 'atar', 'course_code', 'group', 'ese_100_percent']
    df = df[keepvars]
    file = '_'.join([unit.lower(), 'proc', '.csv'])
    df.to_csv(path_data / 'proc' / file)

    return df


def _describe_df(df: pd.DataFrame, unit: str, path_data: Path):
    """Read in processed dataframe. Check scores for IC, AF, and FA==0 grades.
    Sort by cohort, describe continuous and categorical variables, write to TXT.
    Return cleaned dataframe for R analysis and graphs"""
    file = '_'.join([unit.lower(), 'result', '.txt'])
    file = (path_data / 'proc' / file)
    open(file, 'w').close()

    with open(file, 'a') as file:
        file.write('\n>>> Count missing values for any variable\n')
        file.write(df.isnull().groupby(df['group']).sum().astype(int).to_string())
        # bios1168: there are n=2 (group 0; control) who have missing scores
        # bios5090: there are n=1 (group 0; control) & n=2 (group 1; exposed) who have missing scores

        file.write('\n\n>>> Check all IC, AF, grades: set to NaN\n')
        file.write(df.loc[(df['grade'] == 'IC') | (df['grade'] == 'AF')].to_string())
        # set scores to NaN in dataframe
        # bios1168: n=5 (group 1)
        # bios5090: n=2 (group 1) & n=1 (group 0)
        df.loc[(df['grade'] == 'IC') | (df['grade'] == 'AF'), 'ese_100_percent'] = np.nan

        file.write('\n\n>>> Check any FA that is exactly 0. Student enrolled and withdrew but was missed: set to NaN\n')
        file.write(df.loc[(df['grade'] == 'FA') & (df['ese_100_percent'] == 0)].to_string())
        # set scores to NaN in dataframe
        # bios2268: n=1, group 0
        # bios5090: none
        df.loc[(df['grade'] == 'FA') & (df['ese_100_percent'] == 0), 'ese_100_percent'] = np.nan

        file.write('\n\n>>> Count missing values again for any variable\n')
        file.write(df.isnull().groupby(df['group']).sum().astype(int).to_string())
        if unit == 'BIOS1168':
            file.write('\n>>> summary: n=3 (group 0) is sum of 2 original missing, 1 set to missing')
            file.write('\n>>> summary: n=5 (group 1) is sum of 5 set to missing')
            file.write('\n>>> 70-90% of cohort data are available for age, gender, atar, course_code')
        if unit == 'BIOS5090':
            file.write('\n>>> summary: n=1 (group 0); same as first count')
            file.write('\n>>> summary: n=2 (group 1); same as first count')
            file.write('\n>>> Only 15-18% of cohort data are available for age, gender, atar, course_code')

        # summarise variables by group
        file.write('\n\n>>> Summarise variables by group\n')
        file.write('\nVariable: ' + 'sex' + '\n')
        file.write(df['gender'].groupby(df['group']).describe().to_string())
        file.write('\n')
        for i in ['age', 'atar', 'ese_100_percent']:
            file.write('\nVariable: ' + i + '\n')
            file.write(df[i].astype(float).groupby(df['group']).describe().to_string())
            file.write('\n')

    file = '_'.join([unit.lower(), 'clean', '.csv'])
    df.to_csv(path_data / 'proc' / file)
    return df

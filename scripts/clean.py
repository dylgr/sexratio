import pandas as pd

pop_df = pd.read_csv('./data/raw_data/cc-est2021-agesex-all.csv', encoding='iso-8859-1')
loc_df = pd.read_csv('./data/raw_data/2020_Gaz_counties_national.txt', sep='\t')

pop_keep_cols = [
    'GEOID',
    'AGE1519_TOT', 'AGE1519_MALE', 'AGE1519_FEM', 'AGE2024_TOT', 'AGE2024_MALE', 'AGE2024_FEM', 'AGE2529_TOT', 'AGE2529_MALE', 'AGE2529_FEM', 'AGE3034_TOT', 
    'AGE3034_MALE', 'AGE3034_FEM', 'AGE3539_TOT', 'AGE3539_MALE', 'AGE3539_FEM', 'AGE4044_TOT', 'AGE4044_MALE', 'AGE4044_FEM', 'AGE4549_TOT', 'AGE4549_MALE', 
    'AGE4549_FEM', 'AGE5054_TOT', 'AGE5054_MALE', 'AGE5054_FEM', 'AGE5559_TOT', 'AGE5559_MALE', 'AGE5559_FEM', 'AGE6064_TOT', 'AGE6064_MALE', 'AGE6064_FEM',
    'AGE65PLUS_TOT', 'AGE65PLUS_MALE', 'AGE65PLUS_FEM' 
]
pop_df['GEOID'] = 1000*pop_df['STATE'] + pop_df['COUNTY']
#pop_df['GEOID'] = pop_df.
long_pop_df = pop_df.loc[pop_df.YEAR == 3, pop_keep_cols].melt(id_vars=['GEOID'])
long_pop_df[['AGE', 'SEX']] = long_pop_df.variable.str.rsplit('_', 1, expand=True)
long_pop_df['AGE'] = long_pop_df['AGE'].str.replace('AGE', '')
long_pop_df['AGE'] = long_pop_df['AGE'].str[:2] + '-' + long_pop_df['AGE'].str[2:]
long_pop_df['AGE'] = long_pop_df['AGE'].str.replace('-PLUS', '+')
long_pop_df = long_pop_df.pivot(index=['GEOID', 'AGE'], columns='SEX', values='value').reset_index()

loc_keep_cols = ['USPS', 'GEOID', 'NAME', 'INTPTLAT', 'INTPTLONG']
loc_df.columns = loc_df.columns.str.rstrip()
loc_df = loc_df.loc[:, loc_keep_cols]
#loc_df['NAME'] = loc_df['NAME'].str.replace(' Metro Area| Micro Area', '', regex=True)
loc_df = pd.merge(loc_df, pop_df.loc[pop_df.YEAR == 3, ["GEOID", "POPESTIMATE"]], left_on='GEOID', right_on='GEOID', suffixes=(None, '_'))
loc_df.drop(columns='GEOID', inplace=True)
#df = pd.merge(long_pop_df, loc_df, left_on='GEOID', right_on='GEOID', suffixes=(None, '_'))
long_pop_df.to_csv('./data/processed_data/age_data_county.csv')
loc_df.to_csv('./data/processed_data/location_data_county.csv')

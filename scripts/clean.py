import pandas as pd

pop_df = pd.read_csv('./data/raw_data/cbsa-est2021-agesex.csv', encoding='iso-8859-1')
loc_df = pd.read_csv('./data/raw_data/2020_Gaz_cbsa_national.txt', sep='\t')

pop_keep_cols = [
    'CBSA', 'POPESTIMATE', 
    'AGE1519_TOTAL', 'AGE1519_MALE', 'AGE1519_FEMALE', 'AGE2024_TOTAL', 'AGE2024_MALE', 'AGE2024_FEMALE', 'AGE2529_TOTAL', 'AGE2529_MALE', 'AGE2529_FEMALE', 'AGE3034_TOTAL', 
    'AGE3034_MALE', 'AGE3034_FEMALE', 'AGE3539_TOTAL', 'AGE3539_MALE', 'AGE3539_FEMALE', 'AGE4044_TOTAL', 'AGE4044_MALE', 'AGE4044_FEMALE', 'AGE4549_TOTAL', 'AGE4549_MALE', 
    'AGE4549_FEMALE', 'AGE5054_TOTAL', 'AGE5054_MALE', 'AGE5054_FEMALE', 'AGE5559_TOTAL', 'AGE5559_MALE', 'AGE5559_FEMALE', 'AGE6064_TOTAL', 'AGE6064_MALE', 'AGE6064_FEMALE',
    'AGE65PLUS_TOTAL', 'AGE65PLUS_MALE', 'AGE65PLUS_FEMALE' 
]
long_pop_df = pop_df.loc[pop_df.DATE == 3, pop_keep_cols].melt(id_vars=['CBSA', 'POPESTIMATE'])
long_pop_df[['age', 'sex']] = long_pop_df.variable.str.rsplit('_', 1, expand=True)
long_pop_df['age'] = long_pop_df['age'].str.replace('AGE', '')
long_pop_df['age'] = long_pop_df['age'].str[:2] + '-' + long_pop_df['age'].str[2:]
long_pop_df['age'] = long_pop_df['age'].str.replace('-PLUS', '+')

loc_keep_cols = ['GEOID', 'NAME', 'INTPTLAT', 'INTPTLONG']
loc_df.columns = loc_df.columns.str.rstrip()
loc_df = loc_df.loc[:, loc_keep_cols]
loc_df['NAME'] = loc_df['NAME'].str.replace(' Metro Area| Micro Area', '', regex=True)

df = pd.merge(long_pop_df, loc_df, left_on='CBSA', right_on='GEOID', suffixes=(None, '_'))
df.to_csv('./data/processed_data/agesex.csv')
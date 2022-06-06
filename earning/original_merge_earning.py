#
# For ONE TIME merge of exported csv into
# manual spreadsheet at
# https://docs.google.com/spreadsheets/d/1Akq2c1ywZWZmK02lLIYM4QX2ajw9IWVOB5ODR4UmpiA/edit#gid=1487208982

import pandas as pd

dfx = pd.read_csv('export.csv', sep='\t')
dfc = pd.read_csv('totals_current.csv')

dfx['email'] = dfx.email.fillna('').str.strip()
dfc['email'] = dfc.email.fillna('').str.strip()

mf = dfc.merge(dfx, on='email', how='outer')

mf['placeholder'] = ''
mf['total3'] = mf['total2'].fillna(0).astype('int32') + mf['amt'].fillna(0).astype('int32')

mf[['Name', 'email', 'placeholder', 'total1', 'adj', 'total2', 'amt', 'total3', 'wallet']].to_csv('merged.csv', index=False, header=False)


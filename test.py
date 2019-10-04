import pandas as pd
import utils

filenames = [
    'secret/003/003_AIRBOX/003_AIRBOX_20190908_D1_R.csv',
    'secret/003/003_AXIVITY/003_AXIVITY_39129_20190908_D1_R_T+L.csv',
    'secret/003/003_AXIVITY/003_AXIVITY_39129_20190908_D1_R.csv',
    'secret/003/003_EDIMAX/003_EDIMAX_B_20190912_D4_R.xlsx',
    'secret/003/003_EDIMAX/003_EDIMAX_D(O)_20190909_D1_R.xlsx',
    'secret/003/003_EDIMAX/003_EDIMAX_E(I)_20190909_D1_R.xlsx',
    'secret/003/003_HEARTHERMO/003_HEARTHERMO_0186_20190909_D1_R.csv',
    'secret/003/003_HEARTHERMO/003_HEARTHERMO_0186_20190912_D4_R.xlsx',
    'secret/003/003_TEMPPAL/003_TEMPPAL_E_20190909_D1_R.csv',
    'secret/003/003_TEMPPAL/003_TEMPPAL_B_20190911_D3_R.csv',
    'secret/003/003_TEMPPAL/003_TEMPPAL_B_20190912_D4_R.csv',
    'secret/001/001_EDIMAX/001_EDIMAX_C_20190821_D4_R.xlsx'
]

data = pd.read_csv(filenames[0], header=0)
# data = pd.read_csv(filenames[1], header=None)
# data = pd.read_csv(filenames[2], header=None)
# data = pd.read_excel(filenames[3])
# data = pd.read_excel(filenames[4])
# data = pd.read_excel(filenames[5])
# data = pd.read_csv(filenames[6], header=None)
# data = pd.read_excel(filenames[7], header=None)
# data = pd.read_csv(filenames[8], header=0)
# data = pd.read_csv(filenames[9], header=0)
# data = pd.read_csv(filenames[10], skiprows=1, header=None)
# data = pd.read_excel(filenames[11], header=0)

# ""不會影響
# header少一個逗點會影響 （skiprows=1）
# datetime要再處理（excel的日期會自動）

# data = pd.read_csv(filenames[0], header=0)
# data['time'] = data['time'].apply(pd.to_datetime)
# data = pd.read_csv(filenames[1], header=None)
# data[0] = data[0].apply(pd.to_datetime)

print(data.info())
print('--------------------------------')
print(data.head())
print('--------------------------------')
print(data.iloc[0,0])
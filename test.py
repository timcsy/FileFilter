import pandas as pd
import utils
import datetime

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

# df = pd.read_csv(filenames[0], header=None, skiprows=1)
# df = pd.read_csv(filenames[1], header=None)
# df = pd.read_csv(filenames[2], header=None)
# df = pd.read_excel(filenames[3])
# df = pd.read_excel(filenames[4])
# df = pd.read_excel(filenames[5])
df = pd.read_csv(filenames[6], header=None)
# df = pd.read_excel(filenames[7], header=None)
# df = pd.read_csv(filenames[8], header=None, skiprows=1)
# df = pd.read_csv(filenames[9], header=0)
# df = pd.read_csv(filenames[10], skiprows=1, header=None)
# df = pd.read_excel(filenames[11], header=None, skiprows=1)

# ""不會影響
# header少一個逗點會影響 （skiprows=1）
# datetime要再處理（excel的日期會自動）

# df = pd.read_csv(filenames[0], header=0)
# df['time'] = df['time'].apply(pd.to_datetime)
# df = pd.read_csv(filenames[1], header=None)
# df[0] = df[0].apply(pd.to_datetime)

# df = utils.organize_datetime(df, None)
# print(df)
# print('--------------------------------')
# print(df.info())
# print('--------------------------------')
# print(df.head())
# print('--------------------------------')
# print(df.iloc[0,0])

# 小心雖然排序、drop掉了，但是有些欄位名稱是原來的

info = {
    'start': utils.parse_datetime('2019-09-09 02:55:05'),
    'end': utils.parse_datetime('2019-09-09 02:57:48')
}
df = utils.organize_datetime(df, info)
time = info['start']
while time <= info['end']:
    print(time)
    rows = df.loc[(df.iloc[:,0] >= time) & (df.iloc[:,0] < time + datetime.timedelta(seconds=1))]
    print(rows.mean().iloc[0])

    time += datetime.timedelta(seconds=1)
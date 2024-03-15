import os
import pandas as pd
from datetime import datetime, timedelta

path = os.getenv('PATH')

def modelHour_last():
    # df = pd.read_csv('{}/hour.csv'.format(path))
    df = pd.read_csv('../db/hour.csv')
    df['datetime'] = df['group'].apply(lambda x: x.replace(')', ''))
    df['datetime'] = df['datetime'].apply(lambda x: x.replace('(', ''))
    # convertir a datetime con timezone UTC
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['label_d'] = df['datetime'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df['timestamp'] = df['datetime'].apply(lambda x: int(x.timestamp()))
    df['diff'] = df['timestamp'].diff()/3600
    df.fillna(0, inplace=True)
    _df = df.copy()
    df_filter = df.query('engineTime > 1')
    # filtrar los valores de df_filter donde diff sea igual a 1
    # MEJOR ELIMINAMOS VALORES RAROS FEOS
    # df_filter2 = df_filter.query('diff == 1')
    # df_filter = df_filter.query('diff != 1')
    # arr = pd.DataFrame()
    # drop = pd.DataFrame()
    # for i, r in df_filter.iterrows():
    #     c = 0
    #     while (((df.iloc[i]['timestamp']/3600 - df.iloc[i-c]['timestamp']/3600) < r['engineTime']) and (df.iloc[i]['nm'] == df.iloc[i-c]['nm'])):
    #         drop = drop.append(df.iloc[i-c])
    #         c+=1
    #     length = int(r['engineTime'])
    #     for j in range(length + 1):
    #         new_row = r.copy()
    #         new_row['datetime'] = r['datetime'] - timedelta(hours=j)
    #         new_row['consumed'] = r['consumed']/r['engineTime']
    #         new_row['mileage'] = r['mileage']/r['engineTime']
    #         new_row['engineTime'] = r['engineTime']/r['diff']
    #         arr = arr.append(new_row, ignore_index=True)
    # df = df.drop(drop.index)
    # df = df.drop(df_filter2.index)
    # df = df.append(arr, ignore_index=True)
    df = df.drop(df_filter.index)
    df = df.sort_values(by=['datetime'])
    df.reset_index(drop=True, inplace=True)
    df['date'] = df['datetime'].apply(lambda x: x.date())
    df['date'] = pd.to_datetime(df['date'])
    df['label_dt'] = df['datetime'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M'))
    df['label_hr'] = df['label_dt'].apply(lambda x: x.split(' ')[1])
    df['hour'] = df['label_hr'].apply(lambda x: x.split(':')[0]).astype(int)
    df['turn'] = 'day'
    df.loc[(df['hour'] >= 19) | (df['hour'] <= 6), 'turn'] = 'night'
    df.loc[(df['hour'] <= 6), 'date'] = df['date'] - timedelta(days=1)
    df['day'] = df['date'].dt.day_name()
    df['nroday'] = df['day'].replace({'Thursday': 1, 'Friday': 2, 'Saturday': 3, 'Sunday': 4, 'Monday': 5, 'Tuesday': 6, 'Wednesday': 7})
    df['nrohour'] = df['hour'].replace({7: 0, 8: 1, 9: 2, 10: 3, 11: 4, 12: 5, 13: 6, 14: 7, 15: 8, 16: 9, 17: 10, 18: 11, 19: 12, 20: 13, 21: 14, 22: 15, 23: 16, 0: 17, 1: 18, 2: 19, 3: 20, 4: 21, 5: 22, 6: 23})
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['week'] = (df['date'] + pd.offsets.DateOffset(days=-3)).dt.weekofyear
    df['year_week'] = df['year']
    df['month_week'] = df['month']
    df['year_week'] = df.apply(lambda x: 2022 if ((x['week'] == 52) and (x['year'] == 2023)) else x['year'], axis=1)
    df['month_week'] = df.apply(lambda x: 12 if ((x['week'] == 52) and (x['year'] == 2023)) else x['month'], axis=1)
    df['date_week'] = df['date'] - pd.offsets.DateOffset(days=3)
    df['week'] = df['week'].replace(53, 1)
    df['consumed'] = df['consumed'].round(2)
    df['engineTime'] = df['engineTime'].round(2)
    return df

def modelHour():
    df = pd.read_csv('./db/hour.csv')
    df['datetime'] = df['group'].apply(lambda x: x.replace(')', ''))
    df['datetime'] = df['datetime'].apply(lambda x: x.replace('(', ''))
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['date'] = pd.to_datetime(df['date'])
    df['time'] = df['datetime'].apply(lambda x: x.time())
    df['timestamp'] = df['datetime'].apply(lambda x: int(x.timestamp()))
    df['hour'] = df['time'].apply(lambda x: x.hour)
    df['turn'] = 'day'
    df.loc[(df['hour'] >= 19) | (df['hour'] <= 6), 'turn'] = 'night'
    df.loc[(df['hour'] <= 6), 'date'] = df['date'] - timedelta(days=1)
    df['day'] = df['date'].dt.day_name()
    df['nroday'] = df['day'].replace({'Thursday': 1, 'Friday': 2, 'Saturday': 3, 'Sunday': 4, 'Monday': 5, 'Tuesday': 6, 'Wednesday': 7})
    df['nrohour'] = df['hour'].replace({7: 0, 8: 1, 9: 2, 10: 3, 11: 4, 12: 5, 13: 6, 14: 7, 15: 8, 16: 9, 17: 10, 18: 11, 19: 12, 20: 13, 21: 14, 22: 15, 23: 16, 0: 17, 1: 18, 2: 19, 3: 20, 4: 21, 5: 22, 6: 23})
    df['nrodate'] = df['date'] - pd.offsets.DateOffset(days=3)
    df['tmpDay'] = df['date'] - pd.offsets.DateOffset(days=4)
    df['week'] = df['nrodate'].apply(lambda x: x.weekofyear)
    df['month'] = df['date'].apply(lambda x: x.month)
    df['year'] = df['date'].apply(lambda x: x.year)
    df['year_week'] = df['tmpDay'].apply(lambda x: x.year)
    df = df.query('engineTime < 1')
    return df

# df.to_csv('./run/data/hour.csv', index=False)

# # df.query("`{0}` > 10".format(a))
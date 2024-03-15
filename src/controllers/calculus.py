import pandas as pd
import numpy as np
from model.sensorTracing import sensorTracing
from datetime import datetime, timedelta
import time
path='../db'

# quedarme con columnas time y consumoCaudal
def getConsumed(df):
    df1 = df[['Time', 'Speed', 'consumoCaudal', 'Altitude']]
    df1['Time'] = df1['Time'].apply(lambda x: x if len(x) < 6 else np.nan)
    df1.dropna(subset=['Time'], inplace=True)
    df1.reset_index(drop=True, inplace=True)

    df1['datetime'] = pd.to_datetime(df1['Time'].apply(lambda x: x['t']))
    df1['timestamp'] = df1['datetime'].apply(lambda x: time.mktime(x.timetuple()))
    df1['delta'] = df1['timestamp'].diff().shift(-1)
    df1.dropna(subset=['delta'], inplace=True)
    df1['consumo'] = df1['consumoCaudal']/3600 * df1['delta']
    df1['fuelRalenti'] = df1.apply(lambda x: x['consumo'] if x['Speed'] == 0 else 0, axis=1)
    df1['fuelSobrecarga'] = df1.apply(lambda x: x['consumo'] if x['consumoCaudal'] > 123 else 0, axis=1)
    df1['timeRalenti'] = df1.apply(lambda x: x['delta'] if x['Speed'] == 0 else 0, axis=1)
    df1['timeSobrecarga'] = df1.apply(lambda x: x['delta'] if x['consumoCaudal'] > 123 else 0, axis=1)
    volumen = df1['consumo'].sum()
    ralenti = df1.query('Speed == 0')['consumo'].sum()
    sobrecarga = df1.query('consumoCaudal > 123')['consumo'].sum()
    horasRalenti = df1.query('Speed == 0')['delta'].sum()/3600
    horasSobrecarga = df1.query('consumoCaudal > 123')['delta'].sum()/3600
    return volumen, ralenti, sobrecarga, horasRalenti, horasSobrecarga, df1 # galones

def getStops(df):
    stops = []
    stopBegin = []
    detenido = False
    inicio_movimiento = None
    if df['speed'].mean() == 0:
        stops.append({'begin': df['time'][0], 'to': df['time'][len(df)-1]})
    else:
        if df['speed'][0] == 0:
            detenido = True
            inicio_movimiento = df['time'][0]
        for i, r in df.iterrows():
            if r['speed'] == 0 and not detenido:
                inicio_movimiento = r['time']
                stopBegin.append(r['time'])
                detenido = True
            elif r['speed'] > 0 and detenido:
                stops.append({'begin': inicio_movimiento, 'to': df['time'][i-1]})
                detenido = False
            else:
                pass
    df_stops = pd.DataFrame(stops)
    return df_stops
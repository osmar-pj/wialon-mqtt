import pandas as pd
from model.reportGeofence import reportGeofence
from model.sensorTracing import sensorTracing
from controllers.calculus import getStops
from model.stop import getStop
from datetime import datetime, timedelta

def getStopsBetweenTrips(unit, start, end, template):
    df_trips, df_geofences, df_stops, df_parkings = reportGeofence(unit, start, end, template)
    # Calculando # stops de cada viaje
    df = df_trips.copy()
    df['stopsBegin'] = df['end'].apply(lambda x: x['v'])
    df['stopsEnd'] = df['begin'].apply(lambda x: x['v']).shift(-1)
    df.fillna(int((end + timedelta(minutes=1)).timestamp()), inplace=True)
    df['stopsEnd'] = df['stopsEnd'].astype(int)
    df_stops['minLimit'] = df_stops['begin'].apply(lambda x: x['v'])
    df_stops['maxLimit'] = df_stops['to'].apply(lambda x: x['v'])
    df['stops'] = ''
    df['nro_stops'] = 0

    for i, r in df.iterrows():
        timeIn = r['stopsBegin']
        timeOut = r['stopsEnd']
        _df = df_stops.query('minLimit >= @timeIn').query('maxLimit <= @timeOut')
        stops = _df.to_dict('records')
        if len(stops) == 0:
            _df = sensorTracing(unit, datetime.fromtimestamp(timeIn), datetime.fromtimestamp(timeOut))
            stops = getStops(_df).to_dict('records')
        df['stops'][i] = stops
        df['nro_stops'][i] = len(stops)
    return df
import pandas as pd
from model.reportGeofence import reportGeofence
from model.stop import getStop
from datetime import datetime, timedelta
import time

# totalTemplate = 14
# tripTemplate = 13
# grifoTemplate = 15
def getStopsBetweenGeofences(unit, start, end, tempplate):
    df_trips, df = reportGeofence(unit, start, end, tempplate)
    # buscar stops en la ruta
    df['stops'] = ''
    df['nro_stops'] = 0
    for i, r in df.iterrows():
        timeIn = r['timeIn']['v']
        timeOut = r['timeOut']['v']
        start = datetime.fromtimestamp(timeIn) - timedelta(hours=1)
        end = datetime.fromtimestamp(timeOut) + timedelta(hours=1)
        _df = getStop(unit, start, end)
        _df['dateLimitMin']  = _df['begin'].apply(lambda x: x['v'])
        _df['dateLimitMax']  = _df['end'].apply(lambda x: x['v'])
        _df = _df.query('dateLimitMin >= @timeIn').query('dateLimitMax <= @timeOut')
        stops = _df.to_dict('records')
        df['stops'][i] = stops
        df['nro_stops'][i] = len(stops)
        time.sleep(1.5)
    return df
import pandas as pd
from main import login
from model.getResource import getResources
from model.getZones import getZones

df_zones = getZones()
resource = getResources()

def geocerca(zoneId, start, end):
    sdk = login()
    parameterSetLocale = {
        'tzOffset': -18000,
        "language": "en"
    }
    sdk.render_set_locale(parameterSetLocale)
    params = {
        'reportResourceId': resource['items'][0]['id'],
        'reportTemplateId': 11,
        'reportObjectId': resource['items'][0]['id'],
        'reportObjectSecId': int(zoneId),
        'interval': {
            'from': int(start.timestamp()),
            'to': int(end.timestamp()),
            'flags': 117440512
        },
        'remoteExec': 1
    }
    reports = sdk.report_exec_report(params)
    status = sdk.report_get_report_status()
    result = sdk.report_apply_report_result()
    paramsSummary = {
        'tableIndex': 0,
        'config': {
            'type': 'range',
            'data': {
                'from': 0,
                'to': 8,
                'level': 0,
                'unitInfo': 1
            }
        }
    }
    rows = sdk.report_select_result_rows(paramsSummary)
    data = [r['c'] for r in rows]
    df = pd.DataFrame(data)
    df = pd.DataFrame(data)
    df.rename(columns={0: 'nm', 1: 'timeIn', 2: 'timeOut', 3: 'duration', 4: 'parking', 5: 'distance', 6: 'avgSpeed', 7: 'maxSpeed', 8: 'consumed'}, inplace=True)
    df['duration']  = df['duration'].astype(float)
    df['parking']  = df['parking'].astype(float)
    df['distance']  = df['distance'].apply(lambda x: x.split(' ')[0]).astype(float)
    df['avgSpeed']  = df['avgSpeed'].apply(lambda x: x.split(' ')[0]).astype(float)
    df['consumed']  = df['consumed'].apply(lambda x: x.split(' ')[0]).astype(float)
    return df
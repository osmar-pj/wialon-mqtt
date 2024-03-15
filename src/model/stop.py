from calendar import month
import pandas as pd
from main import login
from model.getResource import getResources
from datetime import datetime, timedelta

resources = getResources()

def getStop(unit, start, end):
    sdk = login()
    parameterSetLocale = {
        'tzOffset': -18000,
        "language": "en"
    }
    sdk.render_set_locale(parameterSetLocale)

    paramsExecReport = {
        'reportResourceId': resources['items'][0]['id'],
        'reportTemplateId': 12,
        'reportObjectId': unit,
        'reportObjectSecId': 0,
        'interval': {
            'from': int(start.timestamp()),
            'to': int(end.timestamp()),
            'flags': 117440512
        },
        'remoteExec': 1
    }
    reports = sdk.report_exec_report(paramsExecReport)
    status = sdk.report_get_report_status()
    result = sdk.report_apply_report_result()
    paramsStop = {
        'tableIndex': 0,
        'config': {
            'type': 'range',
            'data': {
                'from': 0,
                'to': result['reportResult']['tables'][0]['rows'],
                'level': 0,
                'unitInfo': 1
            }
        }
    }
    rowsStop = sdk.report_select_result_rows(paramsStop)
    dataStop = [r['c'] for r in rowsStop]
    df_stop = pd.DataFrame(dataStop)
    df_stop.rename(columns={0: 'begin', 1: 'end', 2: 'location'}, inplace=True)
    return df_stop

# pd.set_option('display.max_rows', None)

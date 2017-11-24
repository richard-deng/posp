# coding: utf-8
import datetime

def trans_time(data, datetime_keys):
    if not data:
        return {}

    for key, data_type in datetime_keys:
        if data.get(key):
            if data_type in ('time', 'date'):
                data[key] = str(data[key])
            elif data_type == 'datetime':
                data[key] = data.get(key).strftime('%Y-%m-%d %H:%M:%S')
            else:
                pass
    return data
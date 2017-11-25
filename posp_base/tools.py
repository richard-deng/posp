# coding: utf-8
import datetime
import calendar

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


def gen_trade_table_list(start_time, end_time):

    trade_table_list = []
    start_time = start_time.replace(hour=0, minute=0, second=0)
    while start_time <= end_time:
        trade_table_list.append('record_' + start_time.strftime('%Y%m'))
        mdays = calendar.monthrange(start_time.year, start_time.month)[1]
        start_time = start_time.replace(day=1) + datetime.timedelta(days=mdays)

    return trade_table_list


def gen_from_table(table_list, page, page_size):
    '''
    table_list : {
        'record_201701': 15,
        'record_201702': 23,
        'record_201703': 33,
        'record_201704': 45,
    }
    '''
    origin = [v for k, v in table_list.iteritems()]
    count = sum(origin)
    judge = []
    origin_snd = [0] + origin
    for i, v in enumerate(origin_snd):
        judge[i] = sum(origin[:i+1])

    print count
    print origin
    print origin_snd


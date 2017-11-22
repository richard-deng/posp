# coding: utf-8
import logging
import datetime
from channel import Channel
from zbase.base.dbpool import get_connection_exception

log = logging.getLogger()


class ChannelBind:

    TABLE = 'chnlbind'
    CHNLBIND_MUST_KEY = [
        'userid', 'tradetype', 'chnlid', 'priority',
        '`change`', 'bigmchnt', 'available',
    ]
    CHNLBIND_OPTION_KEY = [
        'mchntid', 'termid', 'mchntnm', 'mcc', 'key1',
        'key2', 'key3', 'chnlfee', 'qffee', 'admin',
        'last_admin', 'create_time', 'update_time',
        'tag1', 'tag2', 'memo', 'id',
    ]
    CHNLBIND_DATETIME_KEY = {
        'create_time': 'datetime',
        'update_time': 'datetime',
    }
    CHNLBIND_KEY = CHNLBIND_MUST_KEY + CHNLBIND_OPTION_KEY

    def __init__(self, chnlbind_id):
        self.id = chnlbind_id
        self.data = {}
        self.keys = ChannelBind.CHNLBIND_KEY

    def load(self):
        where = {'id': self.id}
        with get_connection_exception('posp_core') as conn:
            record = conn.select_one(table=ChannelBind.TABLE, fields=self.keys, where=where)
            self.data = self.trans_time(record)

    @classmethod
    def trans_time(cls, data):

        if not data:
            return {}

        for key, data_type in ChannelBind.CHNLBIND_DATETIME_KEY.iteritems():
            if data.get(key):
                if data_type in ('time', 'date'):
                    data[key] = str(data[key])
                elif data_type == 'datetime':
                    data[key] = data.get(key).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    pass
        return data

    def update(self, values):
        where = {'id': self.id}
        with get_connection_exception('posp_core') as conn:
            ret = conn.update(table=ChannelBind.TABLE, values=values, where=where)
            return ret

    @classmethod
    def create(cls, values):
        with get_connection_exception('posp_core') as conn:
            ret = conn.insert(table=ChannelBind.TABLE, values=values)
            return ret

    @classmethod
    def page(cls, **kwargs):
        need_query = ['userid', 'mchntid', 'termid']
        where = {}
        for k, v in kwargs.iteritems():
            if k in need_query and kwargs.get(k):
                where[cls.TABLE + '.' + k] = kwargs.get(k)
        other = kwargs.get('other', '')
        # if other:
        #    other = 'order by ' + cls.TABLE + '.' + other + 'desc'
        page = kwargs.get('page', 1)
        page_size = kwargs.get('maxnum', 10)
        on = {'chnlbind.chnlid': 'channel.id'}
        keep_fields = [cls.TABLE + '.' + key for key in cls.CHNLBIND_KEY]
        keep_fields.append(Channel.TABLE+'.'+'name')
        with get_connection_exception('posp_core') as conn:
            sql = conn.select_join_sql(
                table1=cls.TABLE,
                table2=Channel.TABLE,
                on=on,
                fields=keep_fields,
                where=where,
            )

            # sql = conn.select_sql(table=cls.TABLE, where=where, fields=cls.CHNLBIND_KEY, other=other)
            pager = conn.select_page(sql, pagecur=page, pagesize=page_size)
            pager.split()
            if pager.count > 0:
                for data in pager.pagedata.data:
                    cls.trans_time(data)
            return pager.pagedata.data, pager.count

    def switch_available(self, available):
        now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
        where = {'id': self.id}
        values = {'available': available, 'update_time': now_str}
        with get_connection_exception('posp_core') as conn:
            ret = conn.update(table=ChannelBind.TABLE, values=values, where=where)
            return ret

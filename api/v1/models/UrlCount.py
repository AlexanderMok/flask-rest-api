# -*- coding: utf-8 -*-
from api.v1.database.db import db


class UrlCountDO(db.Model):
    """
       Model object of DB table r_url_count 
    """
    __tablename__ = 'r_url_count'

    id = db.Column(db.BIGINT, nullable=False, autoincrement=True, primary_key=True)
    record_time = db.Column(db.DATETIME, nullable=False)
    channel_idn = db.Column(db.VARCHAR(128), nullable=False)
    url = db.Column(db.VARCHAR(256), nullable=False)
    req_num = db.Column(db.BIGINT, nullable=False)
    host_name = db.Column(db.VARCHAR(255), nullable=False)
    status_code = db.Column(db.VARCHAR(64), nullable=False)
    sp_code = db.Column(db.VARCHAR(64), nullable=True, default=None)
    all_content = db.Column(db.VARCHAR(1000), nullable=True, default=None)

    def __init__(self, id, record_time, channel_idn, url, req_num, host_name, status_code, sp_code, all_content):
        self.id = id
        self.record_time = record_time
        self.channel_idn = channel_idn
        self.url = url
        self.req_num = req_num
        self.host_name = host_name
        self.status_code = status_code
        self.sp_code = sp_code
        self.all_content = all_content

    def __repr__(self):
        dct = self.__dict__
        lst = ['{}: {}'.format(k, dct[k]) for k in dct]
        return '< {}\n{} >\n'.format(self.__class__.__name__, '\n'.join(lst))

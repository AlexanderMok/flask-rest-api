# -*- coding: utf-8 -*-
from sqlalchemy import cast, Integer
from sqlalchemy import func, SmallInteger

from api.v1.database.db import db
from api.v1.models.UrlCount import UrlCountDO


def find_url_req_num_status(url, sp, begin_time, end_time, page, size):
    """
    
    :param url: 
    :param sp: 
    :param begin_time: 
    :param end_time: 
    :param page: 
    :param size: 
    :return: 
    """
    q = db.session \
        .query(UrlCountDO.url, cast(func.sum(UrlCountDO.req_num), Integer).label('req_num'),
               cast(UrlCountDO.status_code, SmallInteger)) \
        .filter(UrlCountDO.sp_code == sp,
                UrlCountDO.url.like('%{}%'.format(url)),
                UrlCountDO.record_time >= begin_time,
                UrlCountDO.record_time < end_time) \
        .group_by(UrlCountDO.url, UrlCountDO.status_code) \
        .order_by(UrlCountDO.req_num.desc()) \
        .paginate(page, size, error_out=False)
    # [[url,req_num,status],[url,req_num,status]]
    items = []
    for item in q.items:
        url, req_num, status = item
        i = dict(url=url, req_num=req_num, status=status)
        items.append(i)
    result = dict(items=items, total_items=q.total, page=page, per_page=size, totol_pages=q.pages)
    return result


def find_url_req_num(url, sp, begin_time, end_time, page, size):
    """
    
    :param url: 
    :param sp: 
    :param begin_time: 
    :param end_time: 
    :param page: 
    :param size: 
    :return: 
    """

    q = db.session \
        .query(UrlCountDO.url, cast(func.sum(UrlCountDO.req_num), Integer).label('req_num')) \
        .filter(UrlCountDO.sp_code == sp,
                UrlCountDO.url.like('%{}%'.format(url)),
                UrlCountDO.record_time >= begin_time,
                UrlCountDO.record_time < end_time) \
        .group_by(UrlCountDO.url) \
        .order_by(UrlCountDO.req_num.desc()) \
        .paginate(page, size, error_out=False)
    items = []
    for item in q.items:
        url, req_num = item
        i = dict(url=url, req_num=req_num)
        items.append(i)
    result = dict(items=items, total_items=q.total, page=page, per_page=size, totol_pages=q.pages)
    return result


def find_url_status(url, sp, begin_time, end_time, page, size):
    """
    
    :param url: 
    :param sp: 
    :param begin_time: 
    :param end_time: 
    :param page: 
    :param size: 
    :return: 
    """
    q = db.session \
        .query(UrlCountDO.url, cast(UrlCountDO.status_code, SmallInteger)) \
        .filter(UrlCountDO.sp_code == sp,
                UrlCountDO.url.like('%{}%'.format(url)),
                UrlCountDO.record_time >= begin_time,
                UrlCountDO.record_time < end_time) \
        .paginate(page, size, error_out=False)
    items = []
    for item in q.items:
        url, status = item
        i = dict(url=url, status=status)
        items.append(i)
    result = dict(items=items, total_items=q.total, page=page, per_page=size, totol_pages=q.pages)
    return result

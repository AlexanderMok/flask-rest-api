# -*- coding: utf-8 -*-

from sqlalchemy import cast, Integer
from sqlalchemy import func, SmallInteger

from api.v1.database.db import db
from api.v1.models.UrlCount import UrlCountDO


def find_url_req_num_status_page(url, sp, begin_time, end_time, page, size):
    """
    Find url and its associated request num and traffic with paging
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
               cast(UrlCountDO.status_code, SmallInteger), UrlCountDO.record_time) \
        .filter(UrlCountDO.sp_code == sp,
                UrlCountDO.url.like('%{}%'.format(url)),
                UrlCountDO.record_time >= begin_time,
                UrlCountDO.record_time < end_time) \
        .group_by(UrlCountDO.url, UrlCountDO.status_code, UrlCountDO.record_time) \
        .order_by(UrlCountDO.req_num.desc()) \
        .paginate(page, size, error_out=False)
    # [[url,req_num,status],[url,req_num,status]]
    items = []
    for item in q.items:
        url, req_num, status, record_time = item
        i = dict(url=url, req_num=req_num, status=status, record_time=record_time.strftime('%Y-%m-%d  %H:%M:%S'))
        items.append(i)
    result = dict(items=items, total_items=q.total, page=page, per_page=size, totol_pages=q.pages)
    return result


def find_url_req_num_page(url, sp, begin_time, end_time, page, size):
    """
    Find url and its associated request num with paging
    :param url: 
    :param sp: 
    :param begin_time: 
    :param end_time: 
    :param page: 
    :param size: 
    :return: 
    """

    q = db.session \
        .query(UrlCountDO.url, cast(func.sum(UrlCountDO.req_num), Integer).label('req_num'), UrlCountDO.record_time) \
        .filter(UrlCountDO.sp_code == sp,
                UrlCountDO.url.like('%{}%'.format(url)),
                UrlCountDO.record_time >= begin_time,
                UrlCountDO.record_time < end_time) \
        .group_by(UrlCountDO.url, UrlCountDO.record_time) \
        .order_by(UrlCountDO.req_num.desc()) \
        .paginate(page, size, error_out=False)
    items = []
    for item in q.items:
        url, req_num, record_time = item
        i = dict(url=url, req_num=req_num, record_time=record_time.strftime('%Y-%m-%d  %H:%M:%S'))
        items.append(i)
    result = dict(items=items, total_items=q.total, page=page, per_page=size, totol_pages=q.pages)
    return result


def find_url_status_page(url, sp, begin_time, end_time, page, size):
    """
    Find url and its associated status with paging
    :param url: 
    :param sp: 
    :param begin_time: 
    :param end_time: 
    :param page: 
    :param size: 
    :return: 
    """
    q = db.session \
        .query(UrlCountDO.url, cast(UrlCountDO.status_code, SmallInteger), UrlCountDO.record_time) \
        .filter(UrlCountDO.sp_code == sp,
                UrlCountDO.url.like('%{}%'.format(url)),
                UrlCountDO.record_time >= begin_time,
                UrlCountDO.record_time < end_time) \
        .paginate(page, size, error_out=False)
    items = []
    for item in q.items:
        url, status, record_time = item
        i = dict(url=url, status=status, record_time=record_time.strftime('%Y-%m-%d  %H:%M:%S'))
        items.append(i)
    result = dict(items=items, total_items=q.total, page=page, per_page=size, totol_pages=q.pages)
    return result


def find_url_req_num_status_no_page(url, sp, begin_time, end_time):
    """
    Find url and its associated request num and traffic without paging
    :param url: 
    :param sp: 
    :param begin_time: 
    :param end_time: 
    :return: 
    """
    q = db.session \
        .query(UrlCountDO.url, cast(func.sum(UrlCountDO.req_num), Integer).label('req_num'),
               cast(UrlCountDO.status_code, SmallInteger), UrlCountDO.record_time) \
        .filter(UrlCountDO.sp_code == sp,
                UrlCountDO.url.like('%{}%'.format(url)),
                UrlCountDO.record_time >= begin_time,
                UrlCountDO.record_time < end_time) \
        .group_by(UrlCountDO.url, UrlCountDO.status_code, UrlCountDO.record_time) \
        .order_by(UrlCountDO.req_num.desc()).all()
    # [[url,req_num,status],[url,req_num,status]]
    items = list()
    result = dict()
    for item in q:
        # {time: {url1: {status1: {traffic: {}}, {status2 : {traffic:{}}}}
        result.setdefault(item[3], {})
        result[item[3]].setdefault(item[0], {})
        result[item[3]][item[0]].setdefault(item[2], {})
        result[item[3]][item[0]][item[2]].setdefault(item[1], {})
    for time_keys in result:
        record_time = time_keys
        for url_keys in result[time_keys]:
            url = url_keys
            request_info = list()
            for status_keys in result[time_keys][url_keys]:
                status = status_keys
                req_num = [t for t in result[time_keys][url_keys][status_keys]][0]
                d = dict(status=status, req_num=req_num)
                request_info.append(d)
            i = dict(url=url, request_info=request_info, record_time=record_time.strftime('%Y-%m-%d  %H:%M:%S'))
            items.append(i)
    result = dict(items=items)
    return result


def find_url_req_num_no_page(url, sp, begin_time, end_time):
    """
    Find url and its associated request num without paging
    :param url: 
    :param sp: 
    :param begin_time: 
    :param end_time: 
    :return: 
    """

    q = db.session \
        .query(UrlCountDO.url, cast(func.sum(UrlCountDO.req_num), Integer).label('req_num'), UrlCountDO.record_time) \
        .filter(UrlCountDO.sp_code == sp,
                UrlCountDO.url.like('%{}%'.format(url)),
                UrlCountDO.record_time >= begin_time,
                UrlCountDO.record_time < end_time) \
        .group_by(UrlCountDO.url, UrlCountDO.record_time) \
        .order_by(UrlCountDO.req_num.desc()).all()
    items = []
    for item in q:
        url, req_num, record_time = item
        i = dict(url=url, req_num=req_num, record_time=record_time.strftime('%Y-%m-%d  %H:%M:%S'))
        items.append(i)
    result = dict(items=items)
    return result


def find_url_status_no_page(url, sp, begin_time, end_time):
    """
    Find url and its associated status without paging
    :param url: 
    :param sp: 
    :param begin_time: 
    :param end_time: 
    :return: 
    """
    q = db.session \
        .query(UrlCountDO.url, cast(UrlCountDO.status_code, SmallInteger), UrlCountDO.record_time) \
        .filter(UrlCountDO.sp_code == sp,
                UrlCountDO.url.like('%{}%'.format(url)),
                UrlCountDO.record_time >= begin_time,
                UrlCountDO.record_time < end_time).all()
    items = list()
    result = dict()
    for item in q:
        # {time: {url1: set([200, 206]), url2: set([200, 206]), url3: set([200, 206])}}
        result.setdefault(item[2], {})
        result[item[2]].setdefault(item[0], set())
        result[item[2]][item[0]].add(item[1])
    for time_keys in result:
        record_time = time_keys
        for url_keys in result[time_keys]:
            url = url_keys
            status = [l for l in result[time_keys][url_keys]]
            i = dict(url=url, status=status, record_time=record_time.strftime('%Y-%m-%d  %H:%M:%S'))
            items.append(i)
    result = dict(items=items)
    return result

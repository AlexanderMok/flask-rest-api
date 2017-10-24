# -*- coding: utf-8 -*-
import logging

db_config = dict(DBMS='mysql+pymysql',
                 MYSQL_DATABASE_HOST='172.30.40.103',
                 MYSQL_DATABASE_PORT=3306,
                 MYSQL_DATABASE_USER='xxx',
                 MYSQL_DATABASE_PASSWORD='xxx',
                 MYSQL_DATABASE_DB='xxx', )
app_config = {
    'host': '0.0.0.0',
    'port': 5000
}
log_config = {
    'log_path_error': 'openapi.log',
    'log_level': logging.DEBUG
}
API_VERSION_V1 = 'v1'

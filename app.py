# -*- coding: utf-8 -*-
from datetime import timedelta

from flask import Flask

import config
from api.v1 import api_version
from api.v1.database.db import db

app_flask = Flask(__name__)


def _create_app():
    app = _register_blueprints(app_flask)
    app = _configure_app(app)
    app = _set_logging(app)
    return app


def _register_blueprints(app):
    _url_prefix = '/rest/portal/query/api/{version}'.format(version=config.API_VERSION_V1)
    app.register_blueprint(api_version, url_prefix=_url_prefix)
    return app


def _configure_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        '{DBMS}://{username}:{password}@{host}:{port}/{db}'.format(
            DBMS=config.db_config['DBMS'],
            username=config.db_config['MYSQL_DATABASE_USER'],
            password=config.db_config['MYSQL_DATABASE_PASSWORD'],
            host=config.db_config['MYSQL_DATABASE_HOST'],
            port=config.db_config['MYSQL_DATABASE_PORT'],
            db=config.db_config['MYSQL_DATABASE_DB'],
        )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.permanent_session_lifetime = timedelta(days=1)
    db.init_app(app)
    return app


def _set_logging(app):
    import logging
    from logging import handlers
    f_str = '%(asctime)s [%(process)d:%(threadName)s] [%(levelname)s] %(name)s [%(filename)s:%(lineno)d] %(message)s'
    logging.basicConfig(level=config.log_config['log_level'], format=f_str, datefmt='%Y-%m-%d  %H:%M:%S',
                        filename=config.log_config['log_path_error'])
    error_handler = logging.handlers.TimedRotatingFileHandler(config.log_config['log_path_error'],
                                                              encoding='utf-8', when='midnight', utc=True)
    error_handler.setLevel(config.log_config['log_level'])
    app.logger.addHandler(error_handler)
    return app


if __name__ == '__main__':
    _app = _create_app()
    _app.run(host=config.app_config['host'], port=config.app_config['port'], debug=True)

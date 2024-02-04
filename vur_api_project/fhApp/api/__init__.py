# -*- coding: utf-8 -*-
import logging
import warnings

from flask import Blueprint, g

# from zjyApp.db.connect_mysql_server import MysqlConn
# from zjyApp.db.connect_redis_server import RedisConn
from fhApp.db.connect_sql_warehouse import DB_POOL
from fhApp.db.connect_redis_server import RedisConn
from config import router

warnings.filterwarnings("ignore")
logger = logging.getLogger("new_jyzl_screen")

api = Blueprint("vur_pro", __name__, url_prefix=router)

# html = Blueprint("index", __name__, url_prefix=router, static_folder="..{}".format(router))

from . import dbr_view
from . import vhr_view


@api.before_request
def before_request():
    g.db_pool = DB_POOL
    g.db_redis = RedisConn()


@api.teardown_request
def teardown_request(e):
    # g.mysql_cli.dispose()
    pass

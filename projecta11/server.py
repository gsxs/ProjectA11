# coding=utf-8

import os

import tornado.ioloop
import tornado.web
import tornado.locale
from tornado.httpserver import HTTPServer

import projecta11.config as config
import projecta11.db as db
import projecta11.routers as routers
from projecta11.handlers.base import Error404Handler

import projecta11.handlers
# 不能删，handlers 得被载入才会注册好对应的 url pattern


def startup(conf):
    config.conf = conf
    db.startup(conf)

    prev_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    locales_dir = os.path.join(prev_dir, 'locales')
    tornado.locale.load_translations(locales_dir)
    tornado.locale.set_default_locale('zh_CN')

    app = tornado.web.Application(
        routers.get_routers(conf),
        debug=conf.app.debug,
        cookie_secret=conf.app.cookie_secret,
        template_path=conf.app.template_path,
        static_path=conf.app.static_path,
        default_handler_class=Error404Handler)
    if conf.ssl.certfile is not None:
        server = HTTPServer(app, ssl_options={
            "certfile": conf.ssl.certfile,
            "keyfile": conf.ssl.keyfile})
    else:
        server = HTTPServer(app)

    if conf.app.swagger_ui:
        from swagger_ui import tornado_api_doc
        tornado_api_doc(app, config_path='APIv1.yaml', url_prefix='/api/v1/doc',
                        title='Project-A11 RESTful API v1')
    server.listen(conf.app.port)
    tornado.ioloop.IOLoop.current().start()

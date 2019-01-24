# coding=utf-8

import tornado.ioloop
import tornado.web

import projecta11.utils.config as config
import projecta11.utils.db as db
import projecta11.routers as routers

def startup(conf):
    config.conf = conf
    db.startup(conf)

    app = tornado.web.Application(
        routers.get_routers(conf),
        debug=conf.app.debug,
        cookie_secret=conf.app.cookie_secret,
        template_path=conf.app.template_path,
        static_path=conf.app.static_path)
    app.listen(conf.app.port)
    tornado.ioloop.IOLoop.current().start()

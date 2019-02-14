# coding=utf-8

from projecta11.handlers.base import BaseHandler
from projecta11.routers import handling, url


@handling('logout')
class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect(url('index'))

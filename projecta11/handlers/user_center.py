# coding=utf-8

from projecta11.handlers.base import BaseHandler
from projecta11.handlers.decorators import login_needed
from projecta11.routers import handling


@handling(r"/user_center")
class UserCenterHandler(BaseHandler):
    @login_needed
    def get(self):
        self.render("user_center.html", user=self.current_user)

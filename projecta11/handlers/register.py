# coding=utf-8

from projecta11.handlers.base import BaseHandler
import projecta11.utils.db as db
from projecta11.routers import handling, url


@handling(r"/user/register")
class RegisterHandler(BaseHandler):
    def put(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        name = self.get_argument('name')
        role = self.get_argument('role')
        is_male = self.get_argument('is_male')

        if not (username and password and name and role and is_male is not None):
            return self.write('all arguments are required!')
        if not role.isdigit():
            return self.write('role must be an integer!')
        role = int(role)
        if role >= len(db.UserRole.__members__):
            return self.write('illegal role value!')
        role = db.int2role[role]

        # hash the password
        password = self.hash_password(password)

        new_user = db.User(username=username, password=password,
                           name=name, role=role, is_male=bool(is_male))
        self.db_sess.add(new_user)
        self.db_sess.commit()
        self.db_sess.close()

        self.redirect(url('login'))

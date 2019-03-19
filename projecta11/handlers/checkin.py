# coding=utf-8
from json import JSONDecodeError

import sqlalchemy
import time
import random

import projecta11.db as db
from projecta11.config import conf
from projecta11.handlers.base import BaseHandler
from projecta11.routers import handling
from projecta11.utils import require_session, parse_json_body, role_in


@handling(r"/check-in/class/(\d+)/code")
class NewCheckInCodeHandler(BaseHandler):
    @require_session
    @role_in(db.UserRole.teacher)
    def get(self, class_id, sess=None):
        code = random.randint(1000, 9999)
        new_code = db.CheckInCodes(
            code=code,
            class_id=class_id,
            started=False,
            expire_at=int(time.time()))

        self.db.add(new_code)
        try:
            self.db.commit()
        except sqlalchemy.exc.IntegrityError:
            return self.finish(404, 'no matched class_id')

        key = 'checkin:{}'.format(code)
        sess.r.hmset(key, dict(
            code_id=new_code.code_id, class_id=class_id, started=0))

        ret = dict(code_id=new_code.code_id, code=code)
        self.finish(**ret)


@handling(r"/check-in/class/(\d+)/activities/list")
class CheckInActivitiesHandler(BaseHandler):
    @require_session
    @role_in(db.UserRole.teacher)
    def get(self, class_id, sess=None):
        selected = self.db.query(db.CheckInCodes) \
            .filter(db.CheckInCodes.class_id == class_id) \
            .order_by(db.CheckInCodes.expire_at).all()

        list = []
        for i in selected:
            list.append(dict(
                code_id=i.code_id,
                started=i.started,
                expire_at=i.expire_at))

        self.finish(total=len(list), list=list)


@handling(r"/check-in/code/(\d+)/start")
class StartCheckInHandler(BaseHandler):
    @require_session
    @parse_json_body
    @role_in(db.UserRole.teacher)
    def post(self, code_id, data=None, sess=None):
        selected = self.db.query(db.CheckInCodes).filter(
            db.CheckInCodes.code_id == code_id).first()
        if selected is None:
            return self.finish(404, 'no matched code_id')

        wifi_list = data.get('wifi_list')
        if wifi_list is None:
            return self.finish(403, 'missing arguments')

        key1 = 'checkin:{}'.format(selected.code)
        key2 = 'checkin:{}:wifi_list'.format(selected.code)

        sess.r.lpush(key2, *wifi_list)
        sess.r.hmset(key1, {'started': 1})

        sess.r.expire(key1, conf.session.checkin_code_expires_after)
        sess.r.expire(key2, conf.session.checkin_code_expires_after)


@handling(r"/check-in/verify/(\d+)")
class VerifyCheckInCodeHandler(BaseHandler):
    @require_session
    @parse_json_body
    @role_in(db.UserRole.student)
    def put(self, code, data=None, sess=None):
        key1 = 'checkin:{}'.format(code)
        key2 = 'checkin:{}:wifi_list'.format(code)

        teacher_wifi_list = set(map(
            lambda x: x.decode(), sess.r.lrange(key2, 0, -1)))

        try:
            wifi_list = set(data['wifi_list'])
        except JSONDecodeError:
            return self.finish(400, 'error occurred when parsing wifi_list')
        except KeyError:
            return self.finish(403, 'missing arguments')

        if sess.r.exists(key1) and int(sess.r.hget(key1, 'started')) == 1:
            teacher_length = len(teacher_wifi_list)
            num_same = -1
            if teacher_length <= 2*conf.app.wifi_min_same:
                pass
            else:
                num_same = len(teacher_wifi_list.intersection(wifi_list))
                if num_same < conf.app.wifi_min_same:
                    if conf.app.debug:
                        return self.finish(
                            400,
                            "your wifi_list differs from teacher's too much",
                            num_same=num_same)
                    return self.finish(
                        400, "your wifi_list differs from teacher's too much")

            new_log = db.CheckedInLogs(
                code_id=sess.r.hget(key1, 'code_id'), user_id=sess['user_id'])
            self.db.add(new_log)
            self.db.commit()
            self.finish(num_same=num_same)
        else:
            self.finish(404, 'invalid check-in code')


@handling(r"/check-in/verify/code/(\d+)/user/(\d+)")
class CheckInManuallyHandler(BaseHandler):
    @require_session
    @role_in(db.UserRole.teacher)
    def post(self, code_id, user_id, sess=None):
        if self.db.query(db.User).filter(
            db.User.user_id == user_id).first() == None:
            return self.finish(404, 'no such a user_id')

        new_log = db.CheckedInLogs(code_id=code_id, user_id=user_id)
        self.db.add(new_log)
        self.db.commit()


@handling(r"/check-in/code/(\d+)/list")
class CheckedInListHandler(BaseHandler):
    @require_session
    def get(self, code_id, sess=None):
        selected = self.db.query(db.CheckedInLogs, db.User.name).join(db.User) \
            .filter(db.CheckedInLogs.code_id == code_id).all()

        list = []
        for i, user_name in selected:
            user = self.db.query(db.User).filter(
                db.User.user_id == i.user_id).first()
            list.append(dict(
                log_id=i.log_id,
                user_id=user.user_id,
                staff_id=user.staff_id,
                user_name=user_name))

        self.finish(list=list)

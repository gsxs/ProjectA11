# coding=utf-8
import hashlib
from json.decoder import JSONDecodeError

import projecta11.db as db
from projecta11.config import conf
from projecta11.session import Session
from tornado.escape import json_decode


def parse_json_body(func):
    def wrapper(self, *args, **kwargs):
        try:
            data = json_decode(self.request.body)
        except JSONDecodeError:
            self.finish(400, 'bad request')
            return
        return func(self, *args, data=data, **kwargs)
    return wrapper


def require_session(func):
    def wrapper(self, *args, **kwargs):
        session_id = self.get_argument('session_id', None)
        if session_id is None or session_id == '':
            self.finish(403, 'all arguments are required')
            return

        try:
            sess = Session(session_id)
        except FileNotFoundError as e:
            self.finish(402, 'invalid session_id')
            return
        kwargs.update(sess=sess)
        return func(self, *args, **kwargs)
    return wrapper


def role_in(*valid_roles):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            sess = kwargs['sess']
            role = int(sess['role'])
            if role not in map(lambda x: x.value, valid_roles):
                return self.finish(410, 'you have no permission')
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


def keys_filter(obj, keys: [tuple, set]) -> dict:
    if isinstance(obj, dict):
        temp_dict = dict(filter(lambda x: x[0] in keys, obj.items()))
        missing_keys = keys - temp_dict.keys()
        temp_dict.update({key: None for key in missing_keys})
        return temp_dict

    elif isinstance(obj, Session):
        return dict(zip(keys, map(
            lambda x: x.decode() if isinstance(x, bytes) else x,
            obj[keys])))

    elif isinstance(obj, db.Base):
        return {key: obj.__dict__.get(key, None) for key in keys}

    else:
        raise ValueError


def hash_password(password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    salted = hashed + conf.app.password_salt
    hashed_and_salted = hashlib.sha256(salted.encode()).hexdigest()
    return hashed_and_salted

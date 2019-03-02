# coding=utf-8

from projecta11.handlers.base import BaseHandler
from projecta11.routers import handling
from projecta11.handlers import check_code

import io


@handling(r"/captcha")
class CaptchaHandler(BaseHandler):
    def get(self):
        global CODE
        image, CODE = check_code.create_validate_code()
        # BytesIO操作二进制数据，将验证码图形写入内存
        mstream = io.BytesIO()
        image.save(mstream, 'GIF')
        self.write(mstream.getvalue())

import falcon
import sys
import uuid
import json
from model.user import User

class PutPassword(object):
    def on_put(self, req, resp, uid):
        new_user = User()
        password = req.context['body'].get('password')
        new_user.set_uid(uid)
        new_user.set_password(password)
        new_user.write_user_password()
        req.context['result'] = {}
        resp.status = falcon.HTTP_200

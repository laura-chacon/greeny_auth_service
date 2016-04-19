import falcon
import sys
import uuid
import json
from model.user import User

class CreateToken(object):
    def on_post(self, req, resp, uid):
        new_user = User()
        token = str(uuid.uuid4())
        new_user.set_uid(uid)
        new_user.set_token(token)
        new_user.write_user_token()
        body = {'token': token}
        req.context['result'] = body
        resp.status = falcon.HTTP_200

import falcon
import json
import common
from model.user import User
import model.user

class ValidateToken(object):
    def on_get(self, req, resp, uid):
        token = req.get_header('Token')
        user = model.user.try_read(uid)
        if user == None:
            req.context['result'] = {
                'errors': [
                    {'code': "user_not_authorized"}
                ]}
            resp.status = falcon.HTTP_401
        else:
            real_token = user.get_token()
            if real_token == token:
                resp.status = falcon.HTTP_200
            else:
                req.context['result'] = {
                    'errors': [
                        {'code': "user_not_authorized"}
                    ]}
                resp.status = falcon.HTTP_401

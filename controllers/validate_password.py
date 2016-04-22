import falcon
import json
import common
from model.user import User
import model.user

class ValidatePassword(object):
    def on_post(self, req, resp, uid):
        password = req.context['body'].get('password')
        user = model.user.try_read(uid)
        if user == None:
            req.context['result'] = {
                'errors': [
                    {'code': "user_not_found"}
                ]}
            resp.status = falcon.HTTP_404
        else:
            if password == user.get_password():
                token = common.create_token()
                user.set_token(token)
                user.write()
                req.context['result'] = {'token': token}
                resp.status = falcon.HTTP_200
            else:
                req.context['result'] = {
                    'errors': [
                        {'code': "password_invalid"}
                    ]}
                resp.status = falcon.HTTP_401

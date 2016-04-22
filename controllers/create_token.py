import falcon
from model.user import User
import common
import model.user

class CreateToken(object):
    def on_post(self, req, resp, uid):
        user = model.user.try_read(uid)
        if user == None:
            user = User(uid=uid)
        token = common.create_token()
        user.set_token(token)
        user.write()
        req.context['result'] = {'token': token}
        resp.status = falcon.HTTP_200

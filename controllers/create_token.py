import falcon
from model.user import User
import common
import model.user

class CreateToken(object):
    def on_post(self, req, resp, uid):
        user = model.user.try_read(uid)
        if user == None:
            user = User(uid=uid)
        auth_token = common.create_token()
        user.set_token(auth_token)
        user.write()
        req.context['result'] = {'auth_token': auth_token}
        resp.status = falcon.HTTP_200

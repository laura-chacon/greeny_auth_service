import falcon
from model.user import User
import model.user

class PutPassword(object):
    def on_put(self, req, resp, uid):
        password = req.context['body'].get('password')
        user = model.user.try_read(uid)
        if user == None:
            user = User(uid=uid)
        user.set_password(password)
        user.write()
        req.context['result'] = {}
        resp.status = falcon.HTTP_200

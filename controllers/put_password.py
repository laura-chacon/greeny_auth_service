import falcon
from model.user import User

class PutPassword(object):
    def on_put(self, req, resp, uid):
        password = req.context['body'].get('password')
        new_user = User(uid=uid, password=password)
        new_user.write_user_password()
        req.context['result'] = {}
        resp.status = falcon.HTTP_200

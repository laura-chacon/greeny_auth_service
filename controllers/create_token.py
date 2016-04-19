import falcon
import uuid
from model.user import User

class CreateToken(object):
    def on_post(self, req, resp, uid):
        token = str(uuid.uuid4())
        new_user = User(uid=uid, token=token)
        new_user.write_token()
        body = {'token': token}
        req.context['result'] = body
        resp.status = falcon.HTTP_200

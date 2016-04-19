import falcon
import sys
import uuid
import json
from model.user import User

class validate_password(object):
    def on_post(self, req, resp, uid):
        real_password = get_password(uid)
        password = req.context['body'].get('password')
        if password == real_password:
            r = requests.post(
                "http://127.0.0.1:8002/users/" + str(uid) + "/create_token",
                data=json.dumps({}),
                headers={"Content-Type": "application/json",
                         "Accept": "application/json"})
            token = json.loads(r.content)['token']
            req.context['result'] = {'token': token}
            resp.status = falcon.HTTP_200
        else:
            req.context['result'] = {'error': "invalid password"}
            resp.status = falcon.HTTP_401

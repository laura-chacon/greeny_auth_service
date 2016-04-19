import falcon
import json
from controllers.create_token import CreateToken
from controllers.put_password import PutPassword

class RequireJSON(object):
    def process_request(self, req, resp):
        if not req.client_accepts_json:
            raise falcon.HTTPNotAcceptable(
                'This API only supports responses encoded as JSON.',
                href='http://docs.examples.com/api/json')
        if req.method in ('POST', 'PUT'):
            if 'application/json' not in req.content_type:
                raise falcon.HTTPUnsupportedMediaType(
                    'This API only supports requests encoded as JSON.',
                    href='http://docs.examples.com/api/json')


class JSONTranslator(object):
    def process_request(self, req, resp):
        if req.content_length in (None, 0):
            return
        body = req.stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')
        try:
            req.context['body'] = json.loads(body.decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')
    def process_response(self, req, resp, resource):
        if 'result' not in req.context:
            return
        resp.body = json.dumps(req.context['result'])


def add_routes(api):
    api.add_route('/users/{uid}/create_token', CreateToken())
    api.add_route('/users/{uid}/password', PutPassword())


api = falcon.API(middleware=[
    RequireJSON(),
    JSONTranslator(),
])
add_routes(api)

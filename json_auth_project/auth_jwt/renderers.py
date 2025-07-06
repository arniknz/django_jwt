import json

import rest_framework.renderers


class UserJSONRenderer(rest_framework.renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        error = data.get('error', None)
        if error is not None:
            return super(UserJSONRenderer, self).render(data)
        token = data.get('token', None)
        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode('utf-8')

        return json.dumps({
            'user': data
        })

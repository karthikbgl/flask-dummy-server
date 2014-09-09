from flask import Flask
from flask.ext import restful

app = Flask(__name__)
api = restful.Api(app)

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator




class Story(restful.Resource):
    @crossdomain(origin='*')
    def get(self):
        return {'show_url': 'Brian Lehrer',
                'show_pk' : 31655,
                'show_title' : 'Brian Lehrer'
               }

class Stories(restful.Resource):
    def get(self, id=None):
        if not id:
            return [
                {'show_url': '/shows/bl/',
                 'show_pk' : 31655,
                 'show_title' : 'Brian Lehrer'
                },
                {'show_url': '/shows/ll/',
                'show_pk' : 31656,
                'show_title' : 'Leonard Lopate'
                }
            ]
        else:
            return {'show_url': 'Brian Lehrer',
                'show_pk' : 31655,
                'show_title' : 'Brian Lehrer'
               }


api.add_resource(Stories, '/api/v1/story/', endpoint="stories")
api.add_resource(Stories, '/api/v1/story/<id>/', endpoint="story")

api.add_resource(Stories, '/api/v1/stories/', endpoint="stories_")
api.add_resource(Stories, '/api/v1/stories/<id>/', endpoint="story_")

if __name__ == '__main__':
    app.run(debug=True)

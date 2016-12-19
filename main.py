# things.py

# Let's get this party started!
import os
import falcon

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN', 'oi_eu_sou_um_teste')


class ThingsResource(object):

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        print req.params
        if req.params.get('hub.verify_token', '') == VERIFY_TOKEN:
            return req.params.get('hub.challenge', '')
        else:
            return 'Error, wrong validation token'

    def on_post(self, req, resp):
        req.get_data()
        return "ok"


# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
things = ThingsResource()

# things will handle all requests to the '/things' URL path
app.add_route('/', things)

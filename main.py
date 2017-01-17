# things.py

# Let's get this party started!
import os
import json
import falcon
import requests

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN', 'oi_eu_sou_um_teste')
ACCESS_TOKEN = ('EAATZASFZAgRX0BAIOBByLwohSjq5Hy7Ggioky2BRIVd7duCnlA4YZAS1mSo2'
                'IzM1qg3y2XA4C7bf4PsylD1zzCT5yChPzF5MvpXAR4DP14VnXEmkz4DAwkvq0'
                'dTH2N9np9Kg9hhd8gYWLfZBCrDs59VXPsjCjSDZBShH7ZCLQ0kAZDZD')


def reply(user_id, message):

    data = {
        "recipient": {"id": user_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [{
                        "title": "rift",
                        "subtitle": "Next-generation virtual reality",
                        "item_url": "https://www.oculus.com/en-us/rift/",
                        "image_url": "http://messengerdemo.parseapp.com/img/rift.png",
                        "buttons": [{
                            "type": "web_url",
                            "url": "https://www.oculus.com/en-us/rift/",
                            "title": "Open Web URL"
                        }, {
                            "type": "postback",
                            "title": "Call Postback",
                            "payload": "Payload for first bubble"
                        }]
                    }, {
                        "title": "touch",
                        "subtitle": "Your Hands, Now in VR",
                        "item_url": "https://www.oculus.com/en-us/touch/",
                        "image_url": "http://messengerdemo.parseapp.com/img/touch.png",
                        "buttons": [{
                            "type": "web_url",
                            "url": "https://www.oculus.com/en-us/touch/",
                            "title": "Open Web URL"
                        }, {
                            "type": "postback",
                            "title": "Call Postback",
                            "payload": "Payload for second bubble"
                        }]
                    }]
                }
            }
        }
    }
    resp = requests.post('https://graph.facebook.com/v2.8/me/messages?'
                         'access_token=' + ACCESS_TOKEN, json=data)
    print(resp.content)


class ThingsResource(object):

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        print req.params
        if req.params.get('hub.verify_token', '') == VERIFY_TOKEN:
            resp.status = falcon.HTTP_200
            resp.body = req.params.get('hub.challenge', '')
        else:
            resp.body = 'Error, wrong validation token'

    def on_post(self, req, resp):
        print req.params
        print req.context
        data = json.load(req.stream)
        print data
        sender = data['entry'][0]['messaging'][0]['sender']['id']
        print sender
        message = data['entry'][0]['messaging'][0]['message']['text']
        print message
        reply(sender, message)
        resp.status = falcon.HTTP_200


# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
things = ThingsResource()

# things will handle all requests to the '/things' URL path
app.add_route('/', things)

import json
import logging
import uuid
from wsgiref import simple_server

import falcon
#import requests
from api import wordbank, randomizer
#from story import Saver

def load_api(app):

    """ 
    RANDOM STUFF
    """

    bank = wordbank.bank()
    randomizers = randomizer.randomizers(bank)

    for name, rand in randomizers.items():
        app.add_route('/randomapi/{}'.format(name), rand)
        app.add_route('/randomapi/{}/'.format(name), rand)
        app.add_route('/randomapi/%s/{count}'%(name), rand)

    app.add_route('/randomapi/randomizers', ListRandomizer(list(randomizers.keys())))
    app.add_route('/randomapi/batch', MultiRandom(randomizers))
    app.add_route('/randomapi/reload', BankReloader(bank))


class BankReloader():
    def __init__(self, bank):
        self.bank = bank

    #So this shouldn't be attached to get. But I don't care because I just want to 
    #do it quickly with my browser.
    def on_get(self, req, res):
        self.bank.load()
        res.body = "Kicked wordbank"

class ListRandomizer():

    def __init__(self, randomizerNames):
        self.randomizerNames = randomizerNames

    def on_get(self, req, res):
        res.media = self.randomizerNames

class MultiRandom():

    def __init__(self, randomizers):
        self.randomizers = randomizers

    def on_get(self, req, res):
        res.media = [self.getResult(r) for r in req.media]

    def getResult(self, randomizer):
        if randomizer not in self.randomizers:
            return {"name": randomizer, "data": []}
        return self.randomizers[randomizer].get_response()


# If a responder ever raised an instance of StorageError, pass control to
# the given handler.
#app.add_error_handler(StorageError, StorageError.handle)

# Useful for debugging problems in your API; works with pdb.set_trace(). You
# can also use Gunicorn to host your app. Gunicorn can be configured to
# auto-restart workers when it detects a code change, and it also works
# with pdb.
if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8080, app)
    httpd.serve_forever()


import requests
import json
import datetime
from time import sleep

class zKillboard:
    '''
    Defines the api hook into zKillboard.
    '''

    def __init__(self, api_endpoint='https://zkillboard.com/api/'):
        self.api = api_endpoint
        self.session = requests.session()
        self.headers = {
            'Accept-Encoding' : 'gzip',
            'User-Agent' : 'rcooper@nmt.edu | coopss on github'
        }
        self.last_request = datetime.datetime.now()
        self.request_timeout = datetime.timedelta(seconds=1)

    def get(self, endpoint):
        # prevent making too many requests to the server by waiting on a timeout
        while ((datetime.datetime.now() - self.last_request) < self.request_timeout):
            sleep(0)
        # make request
        response = self.session.get(self.api + endpoint, headers=self.headers)
        # update last request time
        self.last_request = datetime.datetime.now()
        # process response code
        if response.status_code != 200:
            raise Exception('Recieved status code %d from %s' % (response.status_code, self.api + endpoint))
        # return json object
        return json.loads(response.text)

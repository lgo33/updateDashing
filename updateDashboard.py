import urllib.request
import json

class updateDashboard(object):
    def __init__(self, host = '192.168.178.34', port = 3030, auth_token = 'YOUR_AUTH_TOKEN'):
        self.url = 'http://' + host + ':' + str(port) + '/widgets/'
        self.auth_token = auth_token

    def update(self, widget, data):
        data['auth_token'] = self.auth_token
        urllib.request.urlopen(self.url + widget, data = json.dumps(data).encode('utf8'))


if __name__ == '__main__':
    updater = updateDashboard(host = '192.168.178.34', auth_token = 'team_luna_2017')
    data = {'text': "updated! this is a very long line ### ### ### ### 123 456 789"}
    updater.update('welcome', data)
    updater.update('humidity', {'value': '44'})

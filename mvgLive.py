from urllib.parse import urlencode, quote
from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys

class mvgLive(object):
    def __init__(self, stop = None, whitelist = None, blacklist = None, maxTime = None) -> object:
        self.setFilter(whitelist=whitelist, blacklist=blacklist, maxTime=maxTime)
        if stop:
            response = self.getResponse(stop)
            self.parsed = self.parse(response.read())



    def getResponse(self, stop, **kwargs):
        return urlopen(self.buildUrl(stop), **kwargs)

    def buildUrl(self, stop, checked=['ubahn', 'bus', 'tram', 'sbahn']):
        url = 'http://www.mvg-live.de/ims/dfiStaticAuswahl.svc?'
        params = {'haltestelle': stop.encode('latin')}
        for method in checked:
            params[method] = 'checked'
        url += urlencode(params)
        return url

    def mkStop(self, params):
        if type(params) == list:
            return {'line': params[0], 'destination': params[1], 'minutes': params[2]}
        else:
            return {'stop': params}

    def setFilter(self, whitelist, blacklist, maxTime):
        self.whitelist = whitelist
        self.blacklist = blacklist
        self.maxTime = maxTime

    def filter(self, stop):
        if self.whitelist:
            if stop['line'] not in self.whitelist and \
                stop['destination'] not in self.whitelist:
                return None
        if self.blacklist:
            if stop['line'] in self.blacklist or \
                stop['destination'] in self.blacklist:
                return None
        if self.maxTime:
            if stop['minutes'] > self.maxTime:
                return None
        return stop

    def parse(self, html):
        soup = BeautifulSoup(html, "html.parser")
        data = {
                'station': None,
                'servertime': None,
                'timetable' : [],
                'alternatives': []
                }
        if soup.find('td', attrs={'class': 'stationColumn'}):
            table = soup.find('table')
            data['station'] = table.find('td', class_='headerStationColumn').text.strip()
            data['servertime'] = table.find('td', class_='serverTimeColumn').text.strip()
            rows = table.find_all('tr', class_=True)
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                add = self.filter(self.mkStop(cols))
                if add:
                    data['timetable'].append(add)
        else:
            try:
                ul = soup.find('ul')
                li = ul.find_all('li')
                for l in li:
                    data['alternatives'].append(self.mkStop(l.text.strip()))
            except AttributeError:
                data['alternatives'] = [self.mkStop('keine Haltestelle gefunden')]
        return data

    def print(self):
        print(self.parsed)

    def usage(self):
        print("python3 mvgLive.py <Haltestelle>")

if __name__ == '__main__':
    #print(quote("Straße aü"))
    #mvg = mvgLive('Grillparzerstraße')
    if len(sys.argv) > 1:
        mvgLive(sys.argv[1]).print()
    else:
        mvgLive().usage()
    #print(mvg.buildUrl('Grillparzerstraße'))

    mvgLive('Grillparzerstraße', whitelist=['100']).print()
    #mvgLive('Grillparzerstraße', blacklist=['54', 'Ostbahnhof']).print()

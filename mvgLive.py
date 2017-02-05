from urllib.parse import urlencode, quote
from urllib.request import urlopen
from bs4 import BeautifulSoup
import sys

class mvgLive(object):
    def __init__(self, stop = None, filter = None) -> object:
        if stop:
            response = self.getResponse(stop)
            self.parsed = self.parse(response.read())
        if filter is not None:
            self.setFilter(filter)


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

    def setFilter(self, filter):
        pass

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
                data['timetable'].append(self.mkStop(cols))
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

    mvgLive('Grillparzerstraße').print()

import requests
import urllib

KEY = 'AIzaSyB7mc9RxZ0oOKdseAC4EeE9WCRC3YI21kQ'
URL = 'https://maps.googleapis.com/maps/api/distancematrix/json?'


def from_office(destination):
    return distance('Burlington Rd, Dublin', destination)


def distance(origin, destination):
    origin = urllib.quote(origin)
    destination = urllib.quote(destination)
    url = '{}origins={}&destinations={}&mode=walking&key={}'\
          .format(URL, origin, destination, KEY)
    response = requests.get(url).json()
    return response['rows'][0]['elements'][0]['duration']['value'] / 60

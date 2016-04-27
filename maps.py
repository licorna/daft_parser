import urllib2

KEY='AIzaSyB7mc9RxZ0oOKdseAC4EeE9WCRC3YI21kQ'
URL='https://maps.googleapis.com/maps/api/distancematrix/json?'

def from_office(destination):
    return distance('Burlington Rd, Dublin', destination)

def distance(origin, destination):
    return 10

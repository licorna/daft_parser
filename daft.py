#!/usr/bin/env python

import fileinput
from defs import parse_attributes, sites

import urllib2

url = 'http://www.daft.ie/dublin/houses-for-rent/rathfarnham/white-church-abbey-rathfarnham-dublin-1637147/'
response = urllib2.urlopen(url)
data = ''.join(response.readlines())

attrs = parse_attributes(data, sites['daft.ie']['attributes'])

print(attrs)

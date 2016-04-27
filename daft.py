#!/usr/bin/env python

import fileinput
from defs import build_collection, parse_attributes, sites

import urllib2

collection = []
with open('saved.htm') as fd:
    collection = build_collection(sites['daft.ie']['collection'],
                                  ''.join(fd.readlines()))

for prop in collection:
    response = urllib2.urlopen(prop)
    data = ''.join(response.readlines())
    print parse_attributes(data, sites['daft.ie']['attributes'])

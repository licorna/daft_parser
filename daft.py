#!/usr/bin/env python

from bs4 import BeautifulSoup as bs
import urllib2
import time
import random
import re
from maps import from_office

from collections import namedtuple

property_attrs = namedtuple('Property', ['shortcode', 'price', 'address',
                                         'rooms', 'furnished', 'd_from_office'])

daft_rental_url = 'http://www.daft.ie/dublin-city/houses-for-rent/south-dublin-city/'

def get_list_of_properties():
    offset = 0
    properties = []
    while True:
        url = daft_rental_url + '?offset=' + str(offset)
        print 'Fetching:', url
        page = urllib2.urlopen(url)
        soup = bs(''.join(page.readlines()), 'html.parser')
        for a in soup.select('.box div h2 a'):
            properties.append(a.attrs['href'])
        if not soup.find('li', class_='next_page') or True:
            break
        offset += 10
        nap = random.randrange(1, 10)
        print 'Sleeping for {} seconds'.format(nap)
        time.sleep(nap)

    return properties

def get_price_from_property(property):
    'property parameter is a soup'
    text_price = property.select('#smi-price-string')[0].text.replace(',', '')
    match = re.search('(\d{3,4})', text_price)
    if match:
        return int(match.group(1))


def get_distance_from_office(address):
    return from_office(address)


def get_address_from_property(property):
    'property parameter is a soup'
    for address in property.select('.map_info_box'):
        match = re.match('^Address: (.*)', address.text)
        if match:
            return match.group(1)


def get_number_of_rooms_from_property(property):
    'property parameter is a soup'
    attrs = get_overview_attributes(property)
    if 'bedrooms' in attrs:
        return int(attrs['bedrooms'])
    return -1


def get_shortcode(property):
    return property.select('.description_extras a[href^="http://www.daft.ie/"]')[0]['href']


def get_is_furnished_from_property(property):
    attrs = get_overview_attributes(property)
    if 'furnished' in attrs:
        return attrs['furnished']
    return False

def get_bedrooms_from_overview(overview):
    match = re.search('(^\d+)', overview)
    if match:
        return match.group(1)

def get_overview_attributes(property):
    attrs = dict(furnished=False)
    for attr in property.select('#overview ul li'):
        if attr.text == 'Furnished':
            attrs['furnished'] = True
        if 'Bedrooms' in attr.text:
            attrs['bedrooms'] = get_bedrooms_from_overview(attr.text)
    return attrs

def get_property_attributes(property_url):
    page = urllib2.urlopen(property_url)
    soup = bs(''.join(page.readlines()), 'html.parser')
    address = get_address_from_property(soup)
    return property_attrs(get_shortcode(soup),
                          get_price_from_property(soup),
                          address,
                          get_number_of_rooms_from_property(soup),
                          get_is_furnished_from_property(soup),
                          get_distance_from_office(address))

if __name__ == '__main__':
    properties = get_list_of_properties()
    print 'Got {} properties'.format(len(properties))
    first = 'http://www.daft.ie' + properties[0]
    print first
    print 'Attributes from first prop:', get_property_attributes(first)

from bs4 import BeautifulSoup as bs
import re
import urllib2
from maps import distance

sites = {
    'daft.ie': {
        'collection': {
            'source': 'https://www.daft.ie/my-daft/saved-ads/',
            'path': 'li.saved-ad',
            'attr': 'data-url',
        },
        'attributes': [
            {
                'path': '#smi-price-string',
                'name': 'monthly price',
                'mask': re.compile('([0-9,]+)'),
                'format': lambda x: int(x.replace(',', ''))
            },
            {
                'path': '#smi-summary-items > .header_text',
                'name': 'beds',
                'selector': lambda x: 'Beds' in x,
                'mask': re.compile('(\d+)'),
                'format': lambda x: int(x)
            },
            # {
            #     'path': '.map_info_box',
            #     'selector': lambda x: 'h3' not in x,
            #     'name': 'walking distance in minutes',
            #     'type': 'int'
            # },
            {
                'path': '.description_extras > a[href^="http://www.daft.ie/"]',
                'name': 'daft_id',
                #'selector': lambda x: 'Beds' in x,
                #'mask': re.compile('(\d+)'),
                #'format': lambda x: int(x)
            },
        ]
    }
}

def build_collection(coll, data):
    #response = urllib2.urlopen(coll['source'])
    #data = ''.join(response.readlines())
    soup = bs(data, 'html.parser')
    response = []
    for prop in soup.select(coll['path']):
        url = prop[coll['attr']]
        if len(url) > 0:
            response.append(url)

    return response

def parse_attributes(data, attrs):
    soup = bs(data, 'html.parser')
    response = []
    for attr in attrs:
        found = find_attribute_in_soup(soup, attr)
        if found:
            response.append((attr['name'], found))

    return response

def find_attribute_in_soup(soup, attr):
    elem = soup.select(attr['path'])
    if attr['name'] == 'walking distance in minutes':
        print elem
    #print elem
    if len(elem) != 1 and 'selector' in attr:
        elem = [e for e in elem if attr['selector'](e.string)][0]
    else:
        elem = elem[0]
    result = elem.string
    if 'mask' in attr:
        elem = attr['mask'].search(elem.string)
        if elem:
            result =  elem.group(0)
    return transform(result, attr)

def transform(text, attr):
    if 'format' not in attr:
        return text
    return attr['format'](text)

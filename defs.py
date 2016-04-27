from bs4 import BeautifulSoup as bs
import re
import urllib2
from maps import distance
import operator

scores = {
    'monthly price': [
        {
            'cond': 'less_than 1800',
            'op': operator.add,
            'qty': 200,
        },
        {
            'cond': 'less_than 2000',
            'op': operator.add,
            'qty': 100,
        },
    ]
}

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
            {
                'path': '.description_extras > a[href^="http://www.daft.ie/"]',
                'name': 'daft_id',
            },
            # {
            #     'path': '.map_info_box',
            #     'selector': lambda x: 'h3' not in x,
            #     'name': 'walking distance in minutes',
            #     'type': 'int'
            # },
        ]
    }
}

def build_collection(coll, data):
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
    if len(elem) == 0:
        return
    if len(elem) != 1 and 'selector' in attr:
        elem = [e for e in elem if attr['selector'](e.string)][0]
    else:
        elem = elem[0]
    if not elem.string:
        return

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

def calc_score(prop, score_def):
    score = 0
    for attr in prop:
        if attr[0] in score_def:
            for rule in score_def[attr[0]]:
                test, value = rule['cond'].split(' ')
                if test == 'less_than':
                    if attr[1] <= int(value):
                        score = rule['op'](score, rule['qty'])
                        break

    return score

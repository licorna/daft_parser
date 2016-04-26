from bs4 import BeautifulSoup as bs
import re

sites = {
    'daft.ie': {
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
            #     'path': 'bla2 bla2',
            #     'name': 'walking distance in minutes',
            #     'type': 'int'
            # },
        ]
    }
}

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

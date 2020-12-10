import os
from sys import argv, stdout
import json
import base64 as b64

def makeItem(query, url, title, subtitle):
    icon = 'icon.png'
    item = {
        'uid': url,
        'title': title,
        'subtitle': subtitle,
        'arg': url,
        'autocomplete': query,
        'icon': {
            'path': icon
        }
    }
    return item

def makeReturn(items):
    out = {
        'items': items
    }
    return out

def main():
    arg_c = len(argv)
    if arg_c <= 1:
        return makeReturn([])
    img = argv[1]
    if not img:
        return makeReturn([])
    with open(img, 'rb') as f:
        ec = str(b64.b64encode(f.read()))
    item = [makeItem(img, ec, 'Encoded String', ec)]
    out = makeReturn(item)
    return json.dumps(out, indent=4) + '\n'

if __name__ == '__main__':
    encoded = main()
    stdout.write(encoded)

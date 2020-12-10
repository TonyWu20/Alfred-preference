import os
from sys import argv, stdout
import json
from urllib.parse import urlparse


def makeItem(query, url, title, subtitle):
    icon = 'polyu.png'
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
    url = argv[1]
    if not url:
        return makeReturn([])
    parse_res = urlparse(url)
    netloc = parse_res[1]
    path = parse_res[2]
    netloc_mod = netloc.replace('.', '-')
    scheme = f"{parse_res[0]}://"
    polyu = ".ezproxy.lb.polyu.edu.hk"
    newurl = scheme + netloc_mod + polyu + path
    item = [makeItem(url, newurl, "Via PolyU", newurl)]
    out = makeReturn(item)
    return json.dumps(out, indent=4) + '\n'


if __name__ == '__main__':
    newurl = main()
    stdout.write(newurl)

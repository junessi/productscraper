#! /usr/bin/python

import requests

headers = {
    'authority': 'www.kramp.com',
    'accept': '*/*',
    'accept-language': 'de,en-US;q=0.9,en;q=0.8,zh;q=0.7,zh-CN;q=0.6',
    'content-type': 'application/json',
    'ctx-corporate-identity': 'kramp',
    'ctx-locale': 'en_DE',
    'origin': 'https://www.kramp.com',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}

json_data = {
    'operationName': 'Categories',
    'variables': {
        'depth': 1,
        'depthAbove1': True,
        'depthAbove2': True,
    },
    'query': 'query Categories($depth: Int!, $depthAbove1: Boolean!, $depthAbove2: Boolean!) {\n  categoryHierarchy(depth: $depth) {\n    id\n    name\n    childCategories @include(if: $depthAbove1) {\n      id\n      name\n      childCategories @include(if: $depthAbove2) {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}',
}

response = requests.post('https://www.kramp.com/graphql/webshop', headers=headers, json=json_data)

print(response.text)
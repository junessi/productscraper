#! /usr/bin/python

import requests
import sys

nargs = len(sys.argv)

if nargs >= 2:
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

    operation_name = sys.argv[1]

    if operation_name == 'Categories' and nargs == 3:
        json_data = {
            'operationName': 'Categories',
            'query': 'query Categories($depth: Int!, $depthAbove1: Boolean!, $depthAbove2: Boolean!) {\n  categoryHierarchy(depth: $depth) {\n    id\n    name\n    childCategories @include(if: $depthAbove1) {\n      id\n      name\n      childCategories @include(if: $depthAbove2) {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}',
            'variables': {
                'depth': int(sys.argv[2]),
                'depthAbove1': True,
                'depthAbove2': True,
            },
        }

    elif operation_name == 'GetChildCategories' and nargs == 3:
        json_data = {
            "operationName": "GetChildCategories",
            "query": "query GetChildCategories($id: ID!) {\n  category(id: $id) {\n    id\n    name\n    childCategories {\n      id\n      name\n      image {\n        src\n        alt\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
            "variables": {"id": "{0}".format(sys.argv[2])}
        }

    elif operation_name == 'GetCategoryProducts' and nargs == 3:
        json_data = {
            'operationName': "GetCategoryProducts",
            'query': 'query GetCategoryProducts($categoryId: ID!, $isAuthenticated: Boolean!, $pageSize: Int!, $page: Int!, $facetValues: FacetValuesInput) {\n  category(id: $categoryId) {\n    id\n    name\n    items(page: $page, pageSize: $pageSize, facetValues: $facetValues) {\n      pagination {\n        page\n        totalPages\n        totalResults\n        __typename\n      }\n      items {\n        id\n        name\n        description\n        brand {\n          id\n          name\n          logo {\n            src\n            alt\n            __typename\n          }\n          __typename\n        }\n        classifications {\n          code\n          values {\n            key\n            value\n            __typename\n          }\n          __typename\n        }\n        image {\n          src\n          alt\n          __typename\n        }\n        quantity\n        roundingQuantity\n        minimumQuantity\n        variant {\n          id\n          name\n          __typename\n        }\n        hasVolumeDiscount @include(if: $isAuthenticated)\n        grossPrice @include(if: $isAuthenticated) {\n          value\n          currency\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}',
            'variables': {
                'categoryId': "{}".format(sys.argv[2]),
                'facetValues': {'multi': [], 'range': [], 'single': []},
                'isAuthenticated': False,
                'page': 1,
                'pageSize': 60
            }
        }

    elif operation_name == 'ProductPage' and nargs == 3:
        json_data = {
            "operationName": "ProductPage",
            "variables": {
                "itemId": "{}".format(sys.argv[2]),
                "isAuthenticated": False
            },
            "query": "query ProductPage($itemId: ID!, $isAuthenticated: Boolean!) {\n  item(id: $itemId) {\n    ... on Item {\n      id\n      name\n      brand {\n        id\n        name\n        logo {\n          src\n          alt\n          __typename\n        }\n        __typename\n      }\n      description\n      image {\n        src\n        alt\n        __typename\n      }\n      grossPrice @include(if: $isAuthenticated) {\n        value\n        currency\n        __typename\n      }\n      classifications {\n        code\n        values {\n          key\n          value\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"
        }
    else:
        print("Unknown arguments:")
        print(sys.argv)
        sys.exit(1)

    # send request
    response = requests.post('https://www.kramp.com/graphql/webshop', headers=headers, json=json_data)
    print(response.text)

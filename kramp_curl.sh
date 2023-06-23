#!/usr/bin/bash

curl 'https://www.kramp.com/graphql/webshop' \
  -H 'authority: www.kramp.com' \
  -H 'accept: */*' \
  -H 'accept-language: de,en-US;q=0.9,en;q=0.8,zh;q=0.7,zh-CN;q=0.6' \
  -H 'content-type: application/json' \
  -H 'ctx-corporate-identity: kramp' \
  -H 'ctx-locale: en_DE' \
  -H 'origin: https://www.kramp.com' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36' \
  --data-raw $'{"operationName":"Categories","variables":{"depth":1,"depthAbove1":true,"depthAbove2":true},"query":"query Categories($depth: Int\u0021, $depthAbove1: Boolean\u0021, $depthAbove2: Boolean\u0021) {\\n  categoryHierarchy(depth: $depth) {\\n    id\\n    name\\n    childCategories @include(if: $depthAbove1) {\\n      id\\n      name\\n      childCategories @include(if: $depthAbove2) {\\n        id\\n        name\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}"}' \


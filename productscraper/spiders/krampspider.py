#!/usr/bin/python3

from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from productscraper.items import ProductItem
from scrapy import Request, Spider
from scrapy.http.request.json_request import JsonRequest
import re
import json
import requests


class KrampSpider(Spider):
    name = 'krampspider'

    def __init__(self):
        self.graphql_url = self.joinurl('/graphql/webshop')

        self.root_item = {'id': 'web1-4045064',
                          'name': 'Agriculture',
                          'parent': '',
                          'type': 'Category'}
        # self.root_item = {'id': 'web2-4045765',
        #                   'name': 'Bio-energy Parts',
        #                   'parent': '',
        #                   'type': 'Category'}
        # self.root_item = {'id': 'web3-113239246',
        #                   'name': 'Grain storage',
        #                   'parent': '',
        #                   'type': 'Category'}
        # self.root_item = {'id': 'web-119905618',
        #                   'name': 'Electric Motor',
        #                   'parent': '',
        #                   'type': 'Category'}

        self.headers = {
            'authority': 'www.kramp.com',
            'accept': '*/*',
            'accept-language': 'de,en-US;q=0.9,en;q=0.8,zh;q=0.7,zh-CN;q=0.6',
            'content-type': 'application/json',
            'ctx-corporate-identity': 'kramp',
            'ctx-locale': 'en_DE',
            'ctx-locale': 'en_DE',
            'origin': 'https://www.kramp.com',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        }

        self.cookies = {'isLoggedIn':'false',
                        'clientInstanceId':'732c31fd-7622-4483-a068-e24c0029c8aa',
                        'USER_LOCALE':'en_DE',
                        'features':'%7B%22de%22%3A%7B%22PoweredByKramp%22%3A%22true%22%2C%22BuyAtMaykers%22%3A%22false%22%2C%22UIRoundedCornerSecondaryButtons%22%3A%22false%22%2C%22OrderSubmitTimeExperimentWeb%22%3A%22false%22%2C%22SearchOnSalesCategoryNameEnabler%22%3A%22true%22%2C%22GuidedSearchPoc%22%3A%22true%22%2C%22FreightCharges%22%3A%22false%22%2C%22InteractedSearchTermCalculationKey%22%3A%22interaction_365d_language%22%2C%22InteractedSearchNoBoundariesEnabler%22%3A%22true%22%2C%22SearchOnSalesCategoryName%22%3A%22control%22%2C%22OrderSubmitTimeExperimentAppEnabler%22%3A%22false%22%2C%22ProductImageViewerEnabler%22%3A%22false%22%2C%22UIBlueLinksEnabler%22%3A%22false%22%2C%22RelatedProductsRedesign%22%3A%22false%22%2C%22AvailabilityV2%22%3A%22false%22%2C%22DeliveryOptionSpecificDeliveryTime%22%3A%22false%22%2C%22SupplementalItems%22%3A%22none%22%2C%22MakeModelSearch%22%3A%22control%22%2C%22UINewFontIconSuiteEnabler%22%3A%22true%22%2C%22InteractedSearchTermSearchSuccessIdentifiersEnabler%22%3A%22true%22%2C%22Chat%22%3A%22false%22%2C%22StockInfo%22%3A%22true%22%2C%22ReducedSearchResults%22%3A%22false%22%2C%22UINewHeaderFooter%22%3A%22true%22%2C%22UINewFontIconSuite%22%3A%22control%22%2C%22UIBackgroundElements%22%3A%22false%22%2C%22InteractedSearchTermSearchSuccessIdentifiers%22%3A%22interaction_365d_language_atc%22%2C%22DeliveryOption%22%3A%22false%22%2C%22FacetsSubmitButton%22%3A%22false%22%2C%22NewProductTable%22%3A%22false%22%2C%22ShoppingCartRecommendations%22%3A%22false%22%2C%22SearchInteractedSearchTerms%22%3A%22true%22%2C%22OrderSubmitTimeExperimentApp%22%3A%22control%22%2C%22RecipientName%22%3A%22false%22%2C%22HideWishlist%22%3A%22false%22%2C%22ProductGroupNavigation%22%3A%22true%22%2C%22UIBlueLinks%22%3A%22variant1%22%2C%22UIBackgroundElementsEnabler%22%3A%22false%22%2C%22UIRoundedCornerSecondaryButtonsEnabler%22%3A%22true%22%2C%22UINewHeaderFooterEnabler%22%3A%22false%22%2C%22ProductGroupNavigationEnabler%22%3A%22false%22%2C%22InteractedSearchTermCalculationKeyEnabler%22%3A%22true%22%2C%22ShowMyAccount%22%3A%22true%22%2C%22Surcharges%22%3A%22false%22%2C%22InteractedSearchNoBoundaries%22%3A%22interaction_365d_language_success%22%2C%22CollapseFacets%22%3A%22false%22%2C%22SearchInteractedSearchTermsEnabler%22%3A%22false%22%2C%22UIRedPrimaryButton%22%3A%22false%22%2C%22ProductImageViewer%22%3A%22false%22%2C%22MakeModelSearchEnabler%22%3A%22false%22%7D%7D',
                        '_vis_opt_exp_0_fired':'1',
                        '_gid':'GA1.2.583251655.1679954887',
                        '_ga_HCT789Y72W':'GS1.1.1679950909.9.1.1679954886.0.0.0',
                        '_gat_UA-5491466-23':'1',
                        'SessionCheck':'1',
                        '_ga':'GA1.2.2102128940.1679954887',
                        'GDPR_COOKIES_ACCEPT':'STANDARD',
                        'ln_or': 'eyIxMjIzMTkzIjoiZCJ9'}

        
    def joinurl(self, path):
        self.protocol = 'https'
        self.domain = 'www.kramp.com'
        return self.protocol + '://' + self.domain + path

    def start_requests(self):
        yield self.query_child_categories(self.root_item['id'])

    def parse_products(self, response):
        try:
            parent_id = response.meta['category_id']
            result = json.loads(response.text)
            facet_id = -1
            facets = result['data']['category']['items']['facets']
            has_categories = False
            for facet in facets:
                facet_id += 1
                if facet['name'] == 'Categories':
                    has_categories = True
                    break

            if has_categories:
                subcategories = facets[facet_id]['values']['values']
                print("{0} subcategories were found".format(len(subcategories)))

                for c in subcategories:
                    c_id = c['key']
                    c_name = c['label']
                    if len(c_id) and len(c_name):
                        product_item = ProductItem()
                        product_item['id'] = c_id
                        product_item['name'] = c_name
                        product_item['parent'] = parent_id
                        product_item['type'] = 'Category'

                        yield ItemLoader(item = product_item).load_item()
                        yield self.query_category_products(c_id)
            else:
                print("query products of {0}".format(result['data']['category']['id']))
                # yield self.query_products(result['data']['category']['id'])
        except Exception as e:
            print("Could not parse item: {0}".format(e))
        return

    def parse_category_products(self, response):
        result = json.loads(response.text)
        category = result['data']['category']
        items = category['items']
        page = items['pagination']['page']
        total_pages = items['pagination']['totalPages']

        for product in items['items']:
            product_item = ProductItem()
            product_item['id'] = product['id']
            product_item['name'] = product['name']
            product_item['parent'] = response.meta['category_id']
            product_item['type'] = 'Product'
            product_item['brand'] = product['brand']['name']
            # print("got item: {0}".format(product_item))
            yield ItemLoader(item = product_item).load_item()

        if page < total_pages:
            yield self.query_category_products(category['id'], page + 1)

    def parse_child_categories(self, response):
        result = json.loads(response.text)
        category = result['data']['category']
        child_categories = category["childCategories"]

        if len(child_categories):
            for cc in child_categories:
                product_item = ProductItem()
                product_item['id'] = cc['id']
                product_item['name'] = cc['name']
                product_item['parent'] = category['id']
                product_item['type'] = 'Category'
                yield ItemLoader(item = product_item).load_item()
                yield self.query_child_categories(cc['id'])
        else:
            yield self.query_category_products(category['id'])

    def query_category(self, category_id):
        graphql_query = {
            "operationName": "ProductFacets",
            "variables": {
                "categoryId": "{0}".format(category_id),
                "facetValues": {
                    "multi": [],
                    "range": [],
                    "single": []
                }
            },
            "query": "query ProductFacets($categoryId: ID!, $facetValues: FacetValuesInput) {\n  category(id: $categoryId) {\n    id\n    breadcrumbs {\n      id\n      title\n      __typename\n    }\n    items(page: 1, pageSize: 60, facetValues: $facetValues) {\n      active_filters {\n        ...ActiveFacetFilterFragment\n        __typename\n      }\n      facets {\n        ...FacetFragment\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ActiveFacetFilterFragment on Filter {\n  field\n  value {\n    __typename\n    ... on ValueFilter {\n      value\n      __typename\n    }\n    ... on ValuesFilter {\n      values\n      __typename\n    }\n    ... on RangeFilter {\n      from\n      to\n      __typename\n    }\n  }\n  __typename\n}\n\nfragment FacetFragment on Facet {\n  name\n  type\n  id\n  values {\n    ... on ValueFacetValues {\n      values {\n        key\n        score\n        label\n        __typename\n      }\n      __typename\n    }\n    ... on RangeFacetValues {\n      unfiltered_min\n      unfiltered_max\n      __typename\n    }\n    __typename\n  }\n  __typename\n}"
        }

        meta = {'category_id': category_id}

        return JsonRequest(url = self.graphql_url,
                           headers = self.headers,
                           data = graphql_query,
                           meta = meta,
                           callback = self.parse_category_products)

    def query_category_products(self, category_id, page = 1, page_size = 60):
        graphql_query = {
            "operationName": "GetCategoryProducts",
            "variables": {
                "categoryId": "{0}".format(category_id),
                "isAuthenticated": False,
                "pageSize": page_size,
                "page": page,
                "facetValues": {
                    "multi": [],
                    "range": [],
                    "single": []
                }
            },
            "query": "query GetCategoryProducts($categoryId: ID!, $isAuthenticated: Boolean!, $pageSize: Int!, $page: Int!, $facetValues: FacetValuesInput) {\n  category(id: $categoryId) {\n    id\n    name\n    items(page: $page, pageSize: $pageSize, facetValues: $facetValues) {\n      pagination {\n        page\n        totalPages\n        totalResults\n        __typename\n      }\n      items {\n        id\n        name\n        description\n        brand {\n          id\n          name\n          logo {\n            src\n            alt\n            __typename\n          }\n          __typename\n        }\n        classifications {\n          code\n          values {\n            key\n            value\n            __typename\n          }\n          __typename\n        }\n        image {\n          src\n          alt\n          __typename\n        }\n        quantity\n        roundingQuantity\n        minimumQuantity\n        variant {\n          id\n          name\n          __typename\n        }\n        hasVolumeDiscount @include(if: $isAuthenticated)\n        grossPrice @include(if: $isAuthenticated) {\n          value\n          currency\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"
        }

        meta = {'category_id': category_id}

        return JsonRequest(url = self.graphql_url,
                           headers = self.headers,
                           data = graphql_query,
                           meta = meta,
                           callback = self.parse_category_products)

    def query_child_categories(self, category_id):
        graphql_query = {
            "operationName": "GetChildCategories",
            "query": "query GetChildCategories($id: ID!) {\n  category(id: $id) {\n    id\n    name\n    childCategories {\n      id\n      name\n      image {\n        src\n        alt\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}",
            "variables": {"id": "{0}".format(category_id)}
        }

        meta = {'category_id': "{0}".format(category_id)}

        return JsonRequest(url = self.graphql_url,
                           headers = self.headers,
                           data = graphql_query,
                           meta = meta,
                           callback = self.parse_child_categories)

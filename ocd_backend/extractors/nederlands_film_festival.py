from ocd_backend.extractors import BaseExtractor, HttpRequestMixin

from lxml import etree

import re


class NederlandsFilmFestivalExtractor(BaseExtractor, HttpRequestMixin):
    def get_collection_objects(self):
        url = self.source_definition['url']

        all_links_xpath = './/div[contains(@class,"photocontainer")]/@rel'

        dates = range(20, 30)
        for date in dates:
            data = {
                '__postback': 'search',
                '__sort': 'date',
                'c_1': '%s/09/17' % (date)
            }
            resp = self.http_session.post('%s/program2017/index.php' % (url), data=data)
            html = etree.HTML(resp.json()['html'])

            # Loop over all div's containg links to item pages
            items = html.xpath(all_links_xpath)

            for item in items:
                data_detail = {
                    '__postback': 'details',
                    'id': item
                }
                resp_detail = self.http_session.get('%s/program2017/index.php?__postback=details&id=%s' % (url, item))
                html_detail = etree.HTML(resp_detail.content)
                link = html_detail.xpath(".//a/@href")
                if link:
                    link = link[0]

                    # Add the base url if the link is a path (which is
                    # always the case afaik)
                    if not link.startswith('http'):
                        link = url + link

                    yield link

    def get_object(self, item_url):
        resp = self.http_session.get(item_url)
        content = re.sub(u'<meta charset="utf-8" />', u'<meta charset="utf-8" />\n<meta name="added_by_osf" property="og:url" content="' + item_url + '" /', resp.content.decode('utf-8'))

        return 'application/html', content

    def run(self):
        for item_url in self.get_collection_objects():
            yield self.get_object(item_url)

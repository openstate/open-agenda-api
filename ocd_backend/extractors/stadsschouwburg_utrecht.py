from ocd_backend.extractors import BaseExtractor, HttpRequestMixin

from lxml import etree

import re


class StadsschouwburgUtrechtExtractor(BaseExtractor, HttpRequestMixin):
    def get_collection_objects(self):
        url = self.source_definition['url']

        all_links_xpath = ".//ul[@class='overview']/li"

        # Continue loop until a page contains no items
        page = 1
        finished = False
        first_item_link = ''
        while not finished:
            resp = self.http_session.get('%s/programma/?p=%s' % (url, str(page)))
            html = etree.HTML(resp.content)

            # Loop over all div's containing links to item pages
            items = html.xpath(all_links_xpath)

            for idx, item in enumerate(items):
                link = item.xpath("h2/a/@href")
                if link:
                    link = link[0]

                    # Add the base url if the link is a path (which is
                    # always the case afaik)
                    if not link.startswith('http'):
                        link = url + link

                    if idx == 0:
                        if first_item_link == link:
                            finished = True
                            break
                        else:
                            first_item_link = link

                    yield link
            page += 1

    def get_object(self, item_url):
        resp = self.http_session.get(item_url)

        # The HTML seems to be encoded in latin-1 instead of utf-8
        return 'application/html', resp.content.decode('iso-8859-1').encode('utf8')

    def run(self):
        for item_url in self.get_collection_objects():
            yield self.get_object(item_url)

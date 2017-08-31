from ocd_backend.extractors import BaseExtractor, HttpRequestMixin

from lxml import etree

import re


class UitagendaUtrechtExtractor(BaseExtractor, HttpRequestMixin):
    def get_collection_objects(self):
        url = self.source_definition['url']

        all_links_xpath = ".//li[@class='entry-post post-performance ']"

        # Continue loop until a page contains no items
        page = 1
        finished = False
        while not finished:
            resp = self.http_session.get('%s/zoeken/?page=%s' % (url, str(page)))
            html = etree.HTML(resp.content)

            # Loop over all elements containing links to item pages
            items = html.xpath(all_links_xpath)

            if not items:
                finised = True
                break

            for item in items:
                link = item.xpath("a/@href")
                if link:
                    link = link[0]

                    # Add the base url if the link is a path (which is
                    # always the case afaik)
                    if not link.startswith('http'):
                        link = url + link

                    yield link
            page += 1

    def get_object(self, item_url):
        resp = self.http_session.get(item_url)

        return 'application/html', resp.content

    def run(self):
        for item_url in self.get_collection_objects():
            yield self.get_object(item_url)

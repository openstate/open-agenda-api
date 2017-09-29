from ocd_backend.extractors import BaseExtractor, HttpRequestMixin

from lxml import etree

import re


class CultuurhuisKanaleneilandExtractor(BaseExtractor, HttpRequestMixin):
    def get_collection_objects(self):
        url = self.source_definition['url']

        all_links_xpath = ".//div[@class='post-content']/div[4]/div/div"

        # Continue loop until a page contains no items
        resp = self.http_session.get('%s/events/' % (url))
        html = etree.HTML(resp.content)

        # Loop over all div's containing links to item pages
        items = html.xpath(all_links_xpath)

        for item in items:
            link = item.xpath("span/a/@href")
            if link:
                link = link[0].strip()

                # Add the base url if the link is a path (which is
                # always the case afaik)
                if not link.startswith('http'):
                    link = url + link

                yield link

    def get_object(self, item_url):
        resp = self.http_session.get(item_url)

        return 'application/html', resp.content

    def run(self):
        for item_url in self.get_collection_objects():
            yield self.get_object(item_url)

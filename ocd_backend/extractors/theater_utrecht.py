from ocd_backend.extractors import BaseExtractor, HttpRequestMixin

from lxml import etree

import json
import re


class TheaterUtrechtExtractor(BaseExtractor, HttpRequestMixin):
    def get_collection_objects(self):
        url = self.source_definition['url']

        all_links_xpath = ".//div[@class='showtime-row']"

        resp = self.http_session.get('%s/agenda' % (url))
        html = etree.HTML(resp.content)

        # Loop over all div's containing links to item pages
        items = html.xpath(all_links_xpath)

        for item in items:
            link = item.xpath("span[@class='showtime-cell title']//a/@href")
            if link:
                link = link[0]

                # Add the base url if the link is a path (which is
                # always the case afaik)
                if not link.startswith('http'):
                    link = url + link

                yield {'url': link, 'agenda': item}

    def get_object(self, item_url):
        resp = self.http_session.get(item_url['url'])

        return_data = {'voorstelling': resp.content, 'agenda': etree.tostring(item_url['agenda'])}
        return 'application/json', json.dumps(return_data)

    def run(self):
        for item_url in self.get_collection_objects():
            yield self.get_object(item_url)

from datetime import datetime
from lxml import etree
import re
import urllib

from ocd_backend.items import BaseItem


class HetFiliaalTheatermakersItem(BaseItem):
    def __init__(self, source_definition, raw_item_content_type, raw_item, item):
        self.main = etree.HTML(item['voorstelling'])
        self.agenda = etree.HTML(item['agenda'])
        super(HetFiliaalTheatermakersItem, self).__init__(source_definition, raw_item_content_type, raw_item, item)

    def get_original_object_id(self):
        # Use slug as object id; some slugs are longer than others so
        # do some checking to find out what parts to use
        slug = self.main.xpath(
            './/meta[@property="og:url"]/@content'
        )[0].split('/')[-2]
        month, year = self.agenda.xpath(
            './/div[contains(@class,"agenda-item")]/@class'
        )[0].split(' ')[1][-7:].split('-')
        day = self.agenda.xpath('.//span[@class="day"]/text()')[0][-2:].strip()
        time = self.agenda.xpath('.//span[@class="time"]/text()')[0].strip()

        return unicode('%s-%s-%s-%sT%s' % (slug, year, month, day, time))

    def get_original_object_urls(self):
        url = unicode(
            self.main.xpath(
                './/meta[@property="og:url"]/@content'
            )[0]
        )

        return {
            'html': url
        }

    def get_rights(self):
        return u'Undefined'

    def get_collection(self):
        return u'Het Filiaal theatermakers'

    def get_combined_index_data(self):
        combined_index_data = {
            'hidden': self.source_definition['hidden']
        }

        return combined_index_data

    def get_index_data(self):
        index_data = {
            '@context': 'https://schema.org',
            '@type': 'TheaterEvent'
        }

        main = self.main
        agenda = self.agenda

        # name
        xpath_query = './/h2[@class="voorstelling-title"]/text()'
        if main.xpath(xpath_query):
            index_data['name'] = unicode(main.xpath(xpath_query)[0].strip())

        # description
        xpath_query = './/h2[@class="voorstelling-title"]/../p//text()'
        if main.xpath(xpath_query):
            index_data['description'] = unicode(' '.join(main.xpath(xpath_query)))

        # location
        xpath_query = './/span[@class="location"]/text()'
        if agenda.xpath(xpath_query):
            index_data['location'] = unicode(agenda.xpath(xpath_query)[0].strip())

        # startDate
        month, year = self.agenda.xpath(
            './/div[contains(@class,"agenda-item")]/@class'
        )[0].split(' ')[1][-7:].split('-')
        day = self.agenda.xpath('.//span[@class="day"]/text()')[0][-2:].strip()
        time = self.agenda.xpath('.//span[@class="time"]/text()')[0].strip()
        index_data['startDate'] = unicode('%s-%s-%sT%s' % (year, month, day, time))

        # image and image contentUrl
        xpath_query = './/div[@class="voorstelling-header"]/@style'
        if main.xpath(xpath_query):
            index_data['image'] = {}
            index_data['image']['@type'] = unicode('ImageObject')
            index_data['image']['contentUrl'] = unicode(re.search("url\('(.*)'\)", main.xpath(xpath_query)[0]).group(1))

        return index_data

    def get_all_text(self):
        text_items = []

        return u' '.join(text_items)

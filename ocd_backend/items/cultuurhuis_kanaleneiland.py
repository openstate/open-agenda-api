from datetime import datetime
import locale
import re
import urllib

from ocd_backend.items import BaseItem


class CultuurhuisKanaleneilandItem(BaseItem):
    locale.setlocale(locale.LC_ALL, 'nl_NL.UTF-8')

    def _get_text_or_none(self, xpath_expression):
        node = self.original_item.find(xpath_expression)
        if node is not None and node.text is not None:
            return unicode(node.text)

    def get_original_object_id(self):
        # Use slug as object id; some slugs are longer than others so
        # do some checking to find out what parts to use
        slug = self.original_item.xpath(
            './/meta[@property="og:url"]/@content'
        )[0].split('/')[-2]

        return unicode(slug)

    def get_original_object_urls(self):
        url = unicode(
            self.original_item.xpath(
                './/meta[@property="og:url"]/@content'
            )[0]
        )

        return {
            'html': url
        }

    def get_rights(self):
        return u'Undefined'

    def get_collection(self):
        return u'Cultuurhuis Kanaleneiland'

    def get_combined_index_data(self):
        combined_index_data = {
            'hidden': self.source_definition['hidden']
        }

        return combined_index_data

    def _nearest(self, items, pivot):
        return min(items, key=lambda x: abs(x - pivot))

    def get_index_data(self):
        index_data = {
            '@context': 'https://schema.org',
            '@type': 'Event'
        }

        main = self.original_item.xpath(".")[0]

        # name
        xpath_query = './/div/div[4]/div/div[2]/div/h1/span/text()'
        if main.xpath(xpath_query):
            index_data['name'] = unicode(main.xpath(xpath_query)[0].strip())

        # description
        xpath_query = './/div/div[4]/div/div[3]/div//text()'
        if main.xpath(xpath_query):
            index_data['description'] = unicode(' '.join(main.xpath(xpath_query)).strip())

        # startDate
        xpath_query = './/div/div[4]/div/div[2]/div/h3/span/text()'
        if main.xpath(xpath_query):
            match_object = re.search('(\d{1,2}) ([^ ]*)$', unicode(main.xpath(xpath_query)[0]))
            day = match_object.group(1).zfill(2)
            month = match_object.group(2)

            # Find the year most likely to belong to the date by
            # adding the previous, current and next year and comparing
            # which date is closest to today's date
            year = datetime.now().year
            this_year = datetime.strptime('%s-%s-%s' % (str(year), month, day), '%Y-%B-%d')
            previous_year = datetime.strptime('%s-%s-%s' % (str(year - 1), month, day), '%Y-%B-%d')
            next_year = datetime.strptime('%s-%s-%s' % (str(year + 1), month, day), '%Y-%B-%d')
            startDate = self._nearest([previous_year, this_year, next_year], datetime.now())
            index_data['startDate'] = startDate.isoformat()[:10]

        # image and image contentUrl
        xpath_query = './/div[contains(@class,"type-page")]/div/div[2]/@style'
        if main.xpath(xpath_query):
            index_data['image'] = {}
            index_data['image']['@type'] = unicode('ImageObject')
            index_data['image']['contentUrl'] = unicode(re.search('url\("(.*)"\)', main.xpath(xpath_query)[0]).group(1))

        return index_data

    def get_all_text(self):
        text_items = []

        return u' '.join(text_items)

from datetime import datetime
import re

from ocd_backend.items import BaseItem


class EKKOItem(BaseItem):
    def _get_text_or_none(self, xpath_expression):
        node = self.original_item.find(xpath_expression)
        if node is not None and node.text is not None:
            return unicode(node.text)

    def get_original_object_id(self):
        # Use slug as object id; some slugs are longer than others so
        # do some checking to find out what parts to use
        slug = self.original_item.xpath(
            ".//meta[@property='og:url']/@content"
        )[0].split('/')[-1]

        return unicode(slug)

    def get_original_object_urls(self):
        url = unicode(
            self.original_item.xpath(".//meta[@property='og:url']/@content")[0]
        )

        return {
            'html': url
        }

    def get_rights(self):
        return u'Undefined'

    def get_collection(self):
        return u'EKKO'

    def get_combined_index_data(self):
        combined_index_data = {
            'hidden': self.source_definition['hidden']
        }

        return combined_index_data

    def get_index_data(self):
        index_data = {
            '@context': 'https://schema.org',
            '@type': 'MusicEvent'
        }

        main = self.original_item.xpath(".")[0]

        pretitle = ''
        xpath_query = './header[@class="articleheader"]/p[@class="pretitle"]/text()'
        if main.xpath(xpath_query):
            pretitle = unicode(main.xpath(xpath_query)[0])

        # name
        xpath_query = './/header[@class="articleheader"]/h2/text()'
        if main.xpath(xpath_query):
            index_data['name'] = unicode(main.xpath(xpath_query)[0])
            if pretitle:
                index_data['name'] = pretitle + ' ' + index_data['name']

        # disambiguatingDescription
        xpath_query = './/header[@class="articleheader"]/p[@class="posttitle"]/text()'
        if main.xpath(xpath_query):
            index_data['disambiguatingDescription'] = unicode(main.xpath(xpath_query)[0])

        # description
        xpath_query = '(.//article[@class="article fullitem"]/div[@class="textholder"])[2]//text()'
        if main.xpath(xpath_query):
            index_data['description'] = unicode(' '.join(main.xpath(xpath_query)).strip())

        # location
        xpath_query = './/div[@class="box box-2 infobox inverted"]//span[@class="location"]/text()'
        if main.xpath(xpath_query):
            index_data['location'] = unicode(main.xpath(xpath_query)[0])

        ## startDate
        # day
        xpath_query = './/div[@class="box box-2 infobox inverted"]//span[@class="date"]/span[@class="day"]/text()'
        if main.xpath(xpath_query):
            day = unicode(main.xpath(xpath_query)[0])

        # month
        xpath_query = './/div[@class="box box-2 infobox inverted"]//span[@class="date"]/span[@class="month"]/text()'
        if main.xpath(xpath_query):
            month = unicode(main.xpath(xpath_query)[0])

        # year
        xpath_query = './/div[@class="box box-2 infobox inverted"]//span[@class="date"]/span[@class="year"]/text()'
        if main.xpath(xpath_query):
            year = unicode(main.xpath(xpath_query)[0])

        # time
        xpath_query = './/div[@class="box box-2 infobox inverted"]//span[@class="date"]/span[@class="time"]/text()'
        if main.xpath(xpath_query):
            times = main.xpath(xpath_query)
            if len(times) == 2:
                index_data['doorTime'] = '%s-%s-%sT%s' % (
                    year,
                    month,
                    day,
                    times[0]
                )
                index_data['startDate'] = '%s-%s-%sT%s' % (
                    year,
                    month,
                    day,
                    times[1]
                )
            else:
                index_data['startDate'] = '%s-%s-%sT%s' % (
                    year,
                    month,
                    day,
                    times[0]
                )

        # image and image contentUrl
        xpath_query = './/article[@class="article fullitem"]/div[@class="imgholder full"]/img/@data-src'
        if main.xpath(xpath_query):
            index_data['image'] = {}
            index_data['image']['@type'] = unicode('ImageObject')
            index_data['image']['contentUrl'] = unicode(
                'https://ekko.nl%s' % (
                    main.xpath(xpath_query)[0]
                )
            )

        return index_data

    def get_all_text(self):
        text_items = []

        return u' '.join(text_items)

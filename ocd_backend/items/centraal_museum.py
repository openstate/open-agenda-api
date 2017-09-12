from datetime import datetime
import locale
import re

from ocd_backend.items import BaseItem


class CentraalMuseumItem(BaseItem):
    locale.setlocale(locale.LC_ALL, 'nl_NL.UTF-8')

    def _get_text_or_none(self, xpath_expression):
        node = self.original_item.find(xpath_expression)
        if node is not None and node.text is not None:
            return unicode(node.text)

    def get_original_object_id(self):
        # Use slug as object id
        return unicode(
            '/'.join(self.original_item.xpath(
                ".//meta[@property='og:url']/@content"
            )[0].split('/')[-3:-1])
        )

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
        return u'Centraal Museum'

    def get_combined_index_data(self):
        combined_index_data = {
            'hidden': self.source_definition['hidden']
        }

        return combined_index_data

    def _extract_date(self, date_string):
        date_regex = '\d{1,2} \w+ \d{4}'
        time_regex = '\d{2}:\d{2}'

        startDate = ''
        endDate = ''

        # Type 1: Match '7 april 2017'
        match = re.match(
            '^({0})$'.format(date_regex),
            date_string.strip()
        )

        if match and len(match.groups()) == 1:
            startDate = unicode(datetime.strptime(match.group(1), '%d %B %Y').isoformat()[:10])
            return 1, startDate, endDate

        # Type 2: Match '7 april 2017 t/m 19 november 2017'
        match = re.match(
            '^({0})\s+t/m\s+({0})$'.format(date_regex),
            date_string.strip()
        )

        if match and len(match.groups()) == 2:
            startDate = unicode(datetime.strptime(match.group(1), '%d %B %Y').isoformat()[:10])
            endDate = unicode(datetime.strptime(match.group(2), '%d %B %Y').isoformat()[:10])
            return 2, startDate, endDate

        # Type 3: Match '25 oktober 2017 14:30u t/m 16:00u'
        match = re.match(
            '^({0})\s+({1})u\s+t/m\s+({1})u$'.format(date_regex, time_regex),
            date_string.strip()
        )

        if match and len(match.groups()) == 3:
            date = unicode(datetime.strptime(match.group(1), '%d %B %Y').isoformat()[:10])
            startDate = '%sT%s' % (date, unicode(match.group(2)))
            endDate = '%sT%s' % (date, unicode(match.group(3)))
            return 3, startDate, endDate

        return 0, startDate, endDate


    def get_index_data(self):
        # Fields follow Schema.org ExhibitionEvent (same as Event) properties
        index_data = {
            'schema.org_type': 'https://schema.org/ExhibitionEvent'
        }

        main = self.original_item.xpath(".//div[@class='main']/div[@class='inner']")[0]

        # name
        if main.xpath('./h2/text()'):
            index_data['name'] = unicode(main.xpath('./h2/text()')[0])

        # disambiguatingDescription, startDate and endDate
        if main.xpath('./p/text()'):
            ptext = main.xpath('./p/text()')
            if len(ptext) == 1:
                date_type, startDate, endDate = self._extract_date(ptext[0])
            if len(ptext) == 2:
                index_data['disambiguatingDescription'] = unicode(ptext[0].strip())
                date_type, startDate, endDate = self._extract_date(ptext[1])

            if date_type == 1:
                index_data['startDate'] = startDate

            if date_type == 2:
                index_data['startDate'] = startDate
                index_data['endDate'] = endDate

            if date_type == 3:
                # This datetime type only occurs for normal events
                index_data['schema.org_type'] = 'https://schema.org/Event'
                index_data['startDate'] = startDate
                index_data['endDate'] = endDate

        # image and image contentUrl
        if main.xpath('./div[@class="imageContainer block"]/img/@src'):
            index_data['image'] = {}
            index_data['image']['schema.org_type'] = unicode('https://schema.org/ImageObject')
            index_data['image']['contentUrl'] = unicode(
                'http://centraalmuseum.nl%s' % (
                    main.xpath('./div[@class="imageContainer block"]/img/@src')[0]
                )
            )

        # image caption
        if main.xpath('./div[@class="imageContainer block"]/div[@class="caption"]/text()'):
            index_data['image']['caption'] = unicode(
                main.xpath('./div[@class="imageContainer block"]/div[@class="caption"]/text()')[0].strip()
            )

        # image creator
        if main.xpath('./div[@class="imageContainer block"]/div[@class="caption"]/p/text()'):
            index_data['image']['creator'] = unicode(
                re.sub(
                    'foto: ',
                    '',
                    main.xpath('./div[@class="imageContainer block"]/div[@class="caption"]/p/text()')[0].strip()
                )
            )

        # description
        if main.xpath('./div[@class="textContent"]//text()'):
            index_data['description'] = unicode(
                ' '.join(main.xpath('./div[@class="textContent"]//text()')).strip()
            )

        return index_data

    def get_all_text(self):
        text_items = []

        return u' '.join(text_items)

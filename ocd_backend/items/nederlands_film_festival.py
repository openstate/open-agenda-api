from datetime import datetime
import locale
import re

from ocd_backend.items import BaseItem


class NederlandsFilmFestivalItem(BaseItem):
    def _get_text_or_none(self, xpath_expression):
        node = self.original_item.find(xpath_expression)
        if node is not None and node.text is not None:
            return unicode(node.text)

    def get_original_object_id(self):
        # Use slug as object id
        return unicode(
            self.original_item.xpath(
                ".//form[@id='ifrm']/@action"
            )[0].rstrip('/').split('/')[-1]
        )

    def get_original_object_urls(self):
        url = unicode(
            self.original_item.xpath(".//form[@id='ifrm']/@action")[0]
        )

        return {
            'html': u'https://www.filmfestival.nl' + url
        }

    def get_rights(self):
        return u'Undefined'

    def get_collection(self):
        return u'Nederlands Film Festival'

    def get_combined_index_data(self):
        combined_index_data = {
            'hidden': self.source_definition['hidden']
        }

        return combined_index_data

    def get_index_data(self):
        index_data = {
            '@context': 'https://schema.org',
            '@type': 'Event'
        }

        # Fields follow Schema.org ScreeningEvent properties if it is a film
        original_object_url = self.get_original_object_urls()
        if "/films/" in original_object_url:
            index_data = {
                '@type': 'ScreeningEvent'
            }

        main = self.original_item.xpath(".")[0]

        # name
        xpath_query = './/div[@class="titlebar"]/h1/text()'
        if main.xpath(xpath_query):
            index_data['name'] = unicode(main.xpath(xpath_query)[0])

        # disambiguatingDescription
        xpath_query = './/span[@id="uTitle_lSubTitle"]/text()'
        if main.xpath(xpath_query):
            index_data['disambiguatingDescription'] = unicode(main.xpath(xpath_query)[0])

        # description
        xpath_query = './/div[@id="ctl03_pInfo"]//text()'
        if main.xpath(xpath_query):
            index_data['description'] = unicode(' '.join(main.xpath(xpath_query)).strip())

        # image and image contentUrl
        xpath_query = '(.//div[@id="slideshow"]/a)[1]/img/@src'
        if main.xpath(xpath_query):
            index_data['image'] = {}
            index_data['image']['@type'] = unicode('ImageObject')
            index_data['image']['contentUrl'] = unicode(
                'https://filmfestival.nl%s' % (
                    main.xpath(xpath_query)[0]
                )
            )

        # year
        year = '2017'

        # dates (our own way to store multiple occurrences of an event)
        occurrences = main.xpath('.//table[@class="scoverview"]//tr[@class="sep"]')
        for occurrence in occurrences:
            xpath_query = '(.//td)[1]/span/text()'
            if occurrence.xpath(xpath_query):
                index_data['location'] = occurrence.xpath(xpath_query)[0].strip()

            xpath_query = '(.//td)[2]/text()'
            if occurrence.xpath(xpath_query):
                date_str = occurrence.xpath(xpath_query)[0].strip() + ' ' + year
                index_data['startDate'] = datetime.strptime(date_str[3:], '%d %b %H.%M %Y').isoformat()[:16]

        #if index_data['@type'] = 'ScreeningEvent':
        #    index_data['workPresented'] = {}
        #    index_data['workPresented']['@type'] = unicode('Movie')
        #    #TODO

        return index_data

    def get_all_text(self):
        text_items = []

        return u' '.join(text_items)

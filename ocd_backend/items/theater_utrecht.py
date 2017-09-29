from datetime import datetime
from lxml import etree
import locale
import re
import urllib

from ocd_backend.items import BaseItem


class TheaterUtrechtItem(BaseItem):
    locale.setlocale(locale.LC_ALL, 'nl_NL.UTF-8')
    def __init__(self, source_definition, raw_item_content_type, raw_item, item):
        self.main = etree.HTML(item['voorstelling'])
        self.agenda = etree.HTML(item['agenda'])
        super(TheaterUtrechtItem, self).__init__(source_definition, raw_item_content_type, raw_item, item)

    def get_original_object_id(self):
        # Use slug as object id; some slugs are longer than others so
        # do some checking to find out what parts to use
        slug = urllib.unquote(self.main.xpath(
            ".//a[@class='button social-button social facebook small']/@href"
        )[0]).split('http://')[-1].split('&')[0].split('/')[-1]
        date = self.agenda.xpath('(.//span[@class="showtime-cell date"]/b)[2]/text()')[0].replace(' ', '-')
        time = self.agenda.xpath('.//span[@class="showtime-cell time"]/text()')[0].strip().replace(' ', '-')

        return unicode('%s-%s-%s' % (slug, date, time))

    def get_original_object_urls(self):
        url = unicode(
            'http://' + urllib.unquote(self.main.xpath(
                ".//a[@class='button social-button social facebook small']/@href"
            )[0]).split('http://')[-1].split('&')[0]
        )

        return {
            'html': url
        }

    def get_rights(self):
        return u'Undefined'

    def get_collection(self):
        return u'Theater Utrecht'

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
        xpath_query = './/h1[@class="js-title"]/text()'
        if main.xpath(xpath_query):
            index_data['name'] = unicode(main.xpath(xpath_query)[0])

        # description
        xpath_query = './/h2[@class="first"]/../p//text()'
        if main.xpath(xpath_query):
            index_data['description'] = unicode(' '.join(main.xpath(xpath_query)))

        # location
        xpath_query = './/span[@class="showtime-cell city"]//text()'
        if agenda.xpath(xpath_query):
            index_data['location'] = unicode(re.sub('\s+', ' ', ' '.join(agenda.xpath(xpath_query))).strip())

        # image and image contentUrl
        xpath_query = './/div[@class="page-header"]/@style'
        if main.xpath(xpath_query):
            index_data['image'] = {}
            index_data['image']['@type'] = unicode('ImageObject')
            index_data['image']['contentUrl'] = unicode('https://www.theaterutrecht.nl' + re.search("url\('(.*)'\)", main.xpath(xpath_query)[0]).group(1))

        ## startDate
        day, month = agenda.xpath('(.//span[@class="showtime-cell date"]/b)[2]/text()')[0][:-1].split(' ')
        time = agenda.xpath('.//span[@class="showtime-cell time"]/text()')[0][:-2].strip()
        # Find the year which belongs to the date by
        # adding the current and next year and comparing
        # which date lies in the future compared to now
        year = datetime.now().year
        this_year = datetime.strptime('%s-%s-%sT%s' % (str(year), month, day, time), '%Y-%b-%dT%H.%M')
        next_year = datetime.strptime('%s-%s-%sT%s' % (str(year + 1), month, day, time), '%Y-%b-%dT%H.%M')
        if this_year > datetime.now():
            index_data['startDate'] = unicode(this_year.isoformat()[:16])
        else:
            index_data['startDate'] = unicode(next_year.isoformat()[:16])

        return index_data

    def get_all_text(self):
        text_items = []

        return u' '.join(text_items)

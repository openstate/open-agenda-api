from datetime import datetime
import json
import microdata
import re

from ocd_backend.items import BaseItem
from convert_microdata import microdataConverter


class UitagendaUtrechtItem(BaseItem):
    def _get_text_or_none(self, xpath_expression):
        node = self.original_item.find(xpath_expression)
        if node is not None and node.text is not None:
            return unicode(node.text)

    def get_original_object_id(self):
        # Use slug as object id; some slugs are longer than others so
        # do some checking to find out what parts to use
        slug = self.original_item.xpath(
            ".//a[@class='i-facebook-share whatsapp no-popup']/@data-link"
        )[0].split('/')[-1]

        return unicode(slug)

    def get_original_object_urls(self):
        url = unicode(self.original_item.xpath(
            ".//a[@class='i-facebook-share whatsapp no-popup']/@data-link"
        )[0])

        return {
            'html': url
        }

    def get_rights(self):
        return u'Undefined'

    def get_collection(self):
        return u'Uitagenda Utrecht'

    def get_combined_index_data(self):
        combined_index_data = {
            'hidden': self.source_definition['hidden']
        }

        return combined_index_data

    def get_index_data(self):
        jsonstr = self.original_item.xpath('(.//script[@type="application/ld+json"]//text())[3]')[0]
        index_data = json.loads(unicode(jsonstr), strict=False)

        return index_data

    def get_all_text(self):
        text_items = []

        return u' '.join(text_items)

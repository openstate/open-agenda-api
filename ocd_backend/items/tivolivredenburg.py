from datetime import datetime
import json
import microdata
import re

from ocd_backend.items import BaseItem
from convert_microdata import microdataConverter


class TivoliVredenburgItem(BaseItem):
    def _get_text_or_none(self, xpath_expression):
        node = self.original_item.find(xpath_expression)
        if node is not None and node.text is not None:
            return unicode(node.text)

    def get_original_object_id(self):
        # Use slug as object id
        return unicode(
            '/'.join(self.original_item.xpath(
                ".//meta[@property='og:url']/@content"
            )[0].split('/')[-2:])
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
        return u'TivoliVredenburg'

    def get_combined_index_data(self):
        combined_index_data = {
            'hidden': self.source_definition['hidden']
        }

        return combined_index_data

    def get_index_data(self):
        index_data = microdataConverter().convert_items(
            json.loads(microdata.get_items(self.data)[0].json())
        )
        index_data['@context'] = 'https://schema.org'

        return index_data

    def get_all_text(self):
        text_items = []

        return u' '.join(text_items)

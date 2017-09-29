from datetime import datetime
import json
import microdata
import re

from ocd_backend.items import BaseItem
from convert_microdata import microdataConverter


class StadsschouwburgUtrechtItem(BaseItem):
    def _get_text_or_none(self, xpath_expression):
        node = self.original_item.find(xpath_expression)
        if node is not None and node.text is not None:
            return unicode(node.text)

    def get_original_object_id(self):
        # Use slug as object id; some slugs are longer than others so
        # do some checking to find out what parts to use
        #slug = self.original_item.xpath(
        #        ".//link[@rel='canonical']/@href"
        #)[0].replace('//', '/').split('/')

        #object_id = ''

        #add_to_id = False
        #for i in slug:
        #    if re.match(r'^\d+$', i) and add_to_id == False:
        #        add_to_id = True
        #    if add_to_id:
        #        object_id += '/' + i

        #return unicode(object_id.lstrip('/'))

        return unicode(re.search('sub-(\d{4})', self.original_item.xpath(".//body/@class")[0]).group(1))

    def get_original_object_urls(self):
        return {
            'html': 'https://www.stadsschouwburg-utrecht.nl/programma/' + self.get_original_object_id()
        }

    def get_rights(self):
        return u'Undefined'

    def get_collection(self):
        return u'Stadsschouwburg Utrecht'

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

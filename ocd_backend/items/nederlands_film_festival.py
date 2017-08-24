from datetime import datetime
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
            'html': 'https://www.filmfestival.nl/' + url
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
        return {}

    def get_all_text(self):
        text_items = []

        return u' '.join(text_items)

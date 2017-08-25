from datetime import datetime
import re
import urllib

from ocd_backend.items import BaseItem


class CultuurhuisKanaleneilandItem(BaseItem):
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

    def get_index_data(self):
        return {}

    def get_all_text(self):
        text_items = []

        return u' '.join(text_items)

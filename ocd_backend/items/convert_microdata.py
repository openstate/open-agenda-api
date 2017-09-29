import json
import microdata


class microdataConverter():
    """
    Extract schema.org items in microdata format
    """
    def convert_items(self, microdata):
        return_data = {}

        if 'type' in microdata:
            return_data['@type'] = microdata['type'][0].split('/')[-1]

        if 'id' in microdata:
            return_data['@id'] = microdata['id']

        if 'properties' in microdata:
            for k, v in microdata['properties'].iteritems():
                if type(v[0]) == unicode:
                    if len(v) == 1:
                        return_data[k] = v[0].strip()
                    else:
                        return_data[k] = v
                elif type(v[0]) == dict:
                    if len(v) == 1:
                        return_data[k] = self.convert_items(v[0])
                    else:
                        return_data[k] = []
                        for item in v:
                            return_data[k].append(self.convert_items(item))

        return return_data

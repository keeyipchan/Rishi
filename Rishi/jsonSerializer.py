from Object import Object
from Rishi.mind import Serializable

__author__ = 'Robur'

import json


class JsonSerializer:
    def serialize(self, obj):
        return json.dumps(self.flatten(obj))

    def flatten(self, obj):
        if isinstance(obj, Object):
            return obj.toFlatObj()
        elif isinstance(obj, list):
            return obj
        elif isinstance(obj, dict):
            res = {}
            for k in obj:
                res[k] = self.flatten(obj[k])
            return res
        return obj

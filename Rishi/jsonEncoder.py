from Rishi.mind import Serializable

__author__ = 'Robur'

import json


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'forJSON'):
            return obj.forJSON()
        else:
            return json.JSONEncoder.default(self,obj)
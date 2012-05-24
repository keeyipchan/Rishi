from Rishi.mind import Serializable

__author__ = 'Robur'

import json


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Serializable):
            return obj.toDict()
        else:
            return json.JSONEncoder.default(self,obj)
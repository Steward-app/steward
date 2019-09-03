from absl import logging

import pymongo
from google.protobuf.json_format import MessageToDict, ParseDict
from bson.objectid import ObjectId

from steward import user_pb2 as u

class StorageManager():
    def __init__(self, env):
        self.mongo_client = pymongo.MongoClient('mongodb://steward.lxc:27017')
        self.db = self.mongo_client['steward-'+env]
        self.users = self.db.user

    def encode(self, proto):
        return self._proto2dict(proto)

    def decode(self, bson, message):
        return self._dict2proto(bson, message)

    def _proto2dict(self, proto):
        logging.debug("proto before conversion: {}".format(proto))
        dict_out = MessageToDict(proto)
        logging.debug("bson dict after conversion: {}".format(dict_out))
        return dict_out

    def _dict2proto(self, bson, message):
        logging.debug("bson dict before conversion: {}".format(bson))
        bson['_id'] = str(bson['_id']) # ObjectId -> str _id
        logging.debug("bson dict after field conversions: {}".format(bson))
        proto = message()
        ParseDict(bson, proto)
        logging.debug("proto after conversion: {}".format(proto))
        return proto

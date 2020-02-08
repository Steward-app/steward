from absl import logging, flags

import pymongo
from google.protobuf.json_format import MessageToDict, ParseDict
from bson.objectid import ObjectId
from bson.errors import InvalidId
from copy import deepcopy

from steward import user_pb2 as u
from steward import maintenance_pb2 as m

FLAGS=flags.FLAGS

flags.DEFINE_enum('env', 'dev', ['dev', 'testing', 'prod'], 'Environment to use.')
flags.DEFINE_string('db', 'mongodb://localhost:27017', 'MongoDB connection string.')

class Collection():
    def __init__(self, collection, proto):
        self.collection = collection
        self.proto = proto
        self.name = proto.DESCRIPTOR.full_name
        logging.info('Collection {0} live'.format(self.name))

    def keys(self):
        return [ str(i) for i in self.collection.distinct('_id')]

    def get_by_attr(self, **kwargs):
        index, key = kwargs.popitem() # only last one is honored
        return self.__getitem__(key, index=index)


    # Convert string key into an ObjectId key compatible with bson
    def _id(self, key):
        try:
            key = ObjectId(key)
        except InvalidId as err:
            raise TypeError(err)
        return key


    def __getitem__(self, key, index='_id'):
        if index == '_id':
            key = self._id(key)
        return self._decode(
                self.collection.find_one({index: key}),
                self.proto)

    def __setitem__(self, key, value):
        key = self._id(key)
        if not isinstance(value, self.proto):
            raise TypeError('{0} is not a valid id')
        value = parent._encode(value)
        return self.collection.find_one({'_id': key})

    def __delitem__(self, key):
        key = self._id(key)
        user = self.__getitem__(key)
        self.collection.delete_one({'_id': key})
        del user['_id'] # unset _id since it won't work anymore
        return user

    def __contains__(self, item):
        item = self._id(item)
        user = self.collection.find_one({'_id': item})
        return user is not None

    def __iter__(self):
        for key in self.keys():
            yield self.__getitem__(key)

    def _encode(self, proto):
        logging.info('Proto->Dict before encode: {}'.format(proto))
        bson = self._proto2dict(proto)
        logging.info('Proto->Dict after encode: {}'.format(bson))
        return bson

    def _decode(self, bson, message):
        logging.info('Dict->Proto before decode: {}'.format(bson))
        proto = self._dict2proto(bson, message)
        logging.info('Dict->Proto after decode: {}'.format(proto))
        return proto

    def _proto2dict(self, proto):
        proto_copy = deepcopy(proto)

        if hasattr(proto, '_id') and proto._id: # existing record, encode it and blank the data
            record_id = ObjectId(proto._id)
            proto_copy._id = '' # does not convert cleanly
        dict_out = MessageToDict(message=proto_copy, preserving_proto_field_name=True)

        if hasattr(proto, '_id') and proto._id: # existing record, need to preserve id
            dict_out['_id'] = record_id
        return dict_out

    def _dict2proto(self, bson, message):
        proto = message()
        if bson and '_id' in bson:
            bson['_id'] = str(bson['_id']) # ObjectId -> str _id
            ParseDict(bson, proto)
        return proto # returns empty if the dict is empty or incompatible


class StorageManager():
    def __init__(self):
        self.mongo_client = pymongo.MongoClient(FLAGS.db)
        database_name = 'steward-' + FLAGS.env
        self.db = self.mongo_client[database_name]
        self.users = Collection(self.db.user, u.User)
        self.maintenances = Collection(self.db.maintenance, m.Maintenance)
        logging.info('StorageManager using {}/{}'.format(FLAGS.db, database_name))

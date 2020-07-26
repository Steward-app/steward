from absl import logging, flags

import pymongo
from google.protobuf.json_format import MessageToDict, ParseDict
from bson.objectid import ObjectId
from bson.errors import InvalidId
from copy import deepcopy

from steward import user_pb2 as u
from steward import maintenance_pb2 as m
from steward import asset_pb2 as a
from steward import schedule_pb2 as s

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
            raise TypeError('{0} is not a valid type of data, expected {1}'.format(value, self.proto))
        value = self._encode(value)
        self.collection.replace_one({'_id': key}, value)
        return self.__getitem__(key)

    def new(self, value):
        if not isinstance(value, self.proto):
            raise TypeError('{0} is not a valid type of data, expected {1}'.format(value, self.proto))
        logging.info('Creating new storage object from ({typeof}): \'{value}\''.format(value=value, typeof=type(value)))
        value = self._encode(value)
        result = self.collection.insert_one(value)
        key = result.inserted_id
        return self.__getitem__(key)

    def __delitem__(self, key):
        key = self._id(key)
        user = self.__getitem__(key)
        self.collection.delete_one({'_id': key})
        item = self._id(item)
        user = self.collection.find_one({'_id': item})
        return user is not None

    def __iter__(self):
        for key in self.keys():
            yield self.__getitem__(key)

    def _encode(self, value):
        logging.debug('Proto->Dict before encode({typeof}): \'{value}\''.format(value=value, typeof=type(value)))
        bson = self._proto2dict(value)
        logging.debug('Proto->Dict after encode: {}'.format(bson))
        return bson

    def _decode(self, bson, message):
        logging.debug('Dict->Proto before decode: {}'.format(bson))
        proto = self._dict2proto(bson, message)
        logging.debug('Dict->Proto after decode: {}'.format(proto))
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
        self.assets = Collection(self.db.asset, a.Asset)
        self.schedules = Collection(self.db.schedule, s.Schedule)

        logging.info('StorageManager using {}/{}'.format(FLAGS.db, database_name))

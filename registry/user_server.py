import time
from concurrent import futures
from absl import logging

import grpc
import pymongo
from google.protobuf.json_format import MessageToDict, ParseDict
from google.protobuf import text_format

from bson.objectid import ObjectId
from bson.json_util import dumps, loads

from steward import user_pb2 as u
from steward import registry_pb2 as r
from steward import user_pb2 as u
from steward import user_pb2_grpc
from steward import registry_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class UserServiceServicer(registry_pb2_grpc.UserServiceServicer):
    def __init__(self, env):
        self.mongo_client = pymongo.MongoClient('mongodb://steward.lxc:27017')
        self.db = self.mongo_client['steward-'+env]
        self.users = self.db.user

    def GetUser(self, request, context):
        id = request._id
        if not isinstance(id, ObjectId):
            id = ObjectId(id)
        print('GetUser id type: {}'.format(type(id)))
        data_bson = self.users.find_one({'_id': id})
        return self.decode(data_bson, u.User)

    def CreateUser(self, request, context):
        user = u.User(name=request.name, email=request.email, password=request.password, available_effort=request.available_effort)
        result = self.users.insert_one(self.encode(user))
        return self.GetUser(u.GetUserRequest(_id=str(result.inserted_id)), None)

    def ListUsers(self, request, context):
        for user_bson in self.users.find():
            user = u.User()
            self.decode(user_bson)
            yield user

    def encode(self, proto):
        return self._proto2dict(proto)

    def decode(self, bson, message):
        return self._dict2proto(bson, message)

    def _proto2dict(self, proto):
        logging.warning("proto before conversion: {}".format(proto))
        dict_out = MessageToDict(proto)
        logging.warning("bson dict after conversion: {}".format(dict_out))
        return dict_out

    def _dict2proto(self, bson, message):
        logging.warning("bson dict before conversion: {}".format(bson))
        bson['_id'] = str(bson['_id']) # ObjectId -> str _id
        logging.warning("bson dict after field conversions: {}".format(bson))
        proto = message()
        ParseDict(bson, proto)
        logging.warning("proto after conversion: {}".format(proto))
        return proto

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    registry_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(env='dev'), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    try:
        while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

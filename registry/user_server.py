import time
from concurrent import futures
from absl import logging

import grpc
import pymongo
from google.protobuf.json_format import MessageToDict, Parse
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
        return self._getUser(request._id)

    def GetUsers(self, request, context):
        yield u.User(_id='deadbeef', name='Seitan', password='********')

    def CreateUser(self, request, context):
        user = u.User(name=request.name, email=request.email, password=request.password)
        result = self.users.insert_one({'proto': '' })
        _id = result.inserted_id
        user._id = str(_id)
        result = self.users.update_one({'_id': _id}, {"$set": { 'proto': user.SerializeToString()}})
        return self._getUser(_id)

    def _getUser(self, id):
        if not isinstance(id, ObjectId):
            id = ObjectId(str(id))
        data_bson = self.users.find_one({'_id': id})
        user = u.User()
        user.ParseFromString(data_bson['proto'])
        return user

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

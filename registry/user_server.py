import time
from concurrent import futures
from absl import logging

import grpc

from bson.objectid import ObjectId
from bson.json_util import dumps, loads

from registry import storage

from steward import user_pb2 as u
from steward import registry_pb2 as r
from steward import user_pb2 as u
from steward import user_pb2_grpc
from steward import registry_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class UserServiceServicer(registry_pb2_grpc.UserServiceServicer):
    def __init__(self, env):
        self.storage = storage.StorageManager(env=env)

    def GetUser(self, request, context):
        id = request._id
        if not isinstance(id, ObjectId):
            id = ObjectId(id)
        print('GetUser id type: {}'.format(type(id)))
        data_bson = self.storage.users.find_one({'_id': id})
        return self.storage.decode(data_bson, u.User)

    def CreateUser(self, request, context):
        user = u.User(name=request.name, email=request.email, password=request.password, available_effort=request.available_effort)
        result = self.storage.users.insert_one(self.storage.encode(user))
        return self.GetUser(u.GetUserRequest(_id=str(result.inserted_id)), None)

    def ListUsers(self, request, context):
        for user_bson in self.storage.users.find():
            user = u.User()
            yield self.storage.decode(user_bson, u.User)

def serve(env):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    registry_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(env=env), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    try:
        while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve(env='dev')

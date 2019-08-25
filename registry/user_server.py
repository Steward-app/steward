import time
import grpc
from absl import logging
from steward import user_pb2, user_pb2_grpc, registry_pb2, registry_pb2_grpc
from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class UserServiceServicer(registry_pb2_grpc.UserServiceServicer):
    def GetUser(self, request, context):
        if request.id == 42:
            return user_pb2.User(id=42, name="pertti", password="keinonen")
        else:
            return user_pb2.User(id=-1, name="")

    def GetUsers(self, request, context):
        yield user_pb2.User(id=666, name="Seitan", password="********")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    registry_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    try:
        while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

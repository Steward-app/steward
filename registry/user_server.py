import time
import grpc
from absl import logging
from steward import user_pb2, user_pb2_grpc
from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class UserServicer(user_pb2_grpc.UserServicer):
    def GetUser(self, request, context):
        if request.id == 42:
            return user_pb2.UserResponse(id=42, name="pertti", level=user_pb2.OWNER)
        else:
            return user_pb2.UserResponse(id=-1, name="", level=user_pb2.ANONYMOUS)

    def GetUsers(self, request, context):
        yield user_pb2.UserResponse(id=666, name="Seitan", level=user_pb2.USER)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    try:
        while True:
                time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

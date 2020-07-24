from concurrent import futures
from absl import logging, flags, app

import grpc
from grpc_reflection.v1alpha import reflection

from registry import storage, server_flags
from registry.decorators import must_have, must_have_any

from steward import user_pb2 as u
from steward import registry_pb2_grpc, registry_pb2

FLAGS = flags.FLAGS

class UserServiceServicer(registry_pb2_grpc.UserServiceServicer):
    def __init__(self, storage_manager=None, argv=None):
        if not storage_manager:
            self.storage = storage.StorageManager()
        else:
            self.storage = storage_manager
        logging.info('UserService initialized.')

    @must_have_any(['_id', 'email'], u.User)
    def GetUser(self, request, context):
        user_id = request._id
        email = request.email
        if user_id:
            return self.storage.users[user_id]
        elif email:
            return self.storage.users.get_by_attr(email=email)

        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details('User "{}" not found.'.format(request))
        return u.User()

    @must_have('email', u.User)
    @must_have('name', u.User)
    @must_have('password', u.User)
    def CreateUser(self, request, context):
        # only create if user doesn't exist
        existing_user = self.storage.users.get_by_attr(email=request.email)
        if existing_user == u.User():
            user = u.User(name=request.name, email=request.email, password=request.password, available_effort=request.available_effort)
            return self.storage.users.new(user)
        else:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details('User "{}" already exists.'.format(request.email))
            return u.User()

    @must_have('_id', u.User)
    def UpdateUser(self, request, context):
        user_id = request._id
        # only update if user exists
        existing_user = self.storage.users[user_id]
        if user is not u.User(): # if not empty
            logging.info('UpdateUser, before update in dict: {}'.format(user))
            user.MergeFrom(request.user)
            logging.info('UpdateUser, merged Proto: {}'.format(user))
            result = self.storage.users[user_id] = user
            return self.GetUser(u.GetUserRequest(_id=user_id), context)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User id "{}" does not exist.'.format(user_id))
            return u.User()

    @must_have('_id', u.User)
    def DeleteUser(self, request, context):
        user_id = request._id

        # only delete if user exists and we need to return the deleted user anyway
        user = self.storage.users[user_id]
        if user != u.User():
            del self.storage.users[user_id]
            return user
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User id "{}" does not exist.'.format(user_id))
            return u.User()

    def ListUsers(self, request, context):
        for user in self.storage.users:
            yield user

def serve(argv):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    registry_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)
    SERVICE_NAMES = (
            registry_pb2.DESCRIPTOR.services_by_name['UserService'].full_name,
            reflection.SERVICE_NAME,
            )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port(FLAGS.listen_addr)
    logging.info('User Microserver listening to: {0}'.format(FLAGS.listen_addr))
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    app.run(serve)

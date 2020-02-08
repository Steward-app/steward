from concurrent import futures
from absl import logging, flags, app

import grpc
from grpc_reflection.v1alpha import reflection

from bson.objectid import ObjectId
from bson.json_util import dumps, loads

from registry import storage, server_flags

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

    def GetUser(self, request, context):
        user_id = request._id
        email = request.email
        if user_id:
            user = self.storage.users[user_id]
        elif email:
            user = self.storage.users[email]
        else:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('No search parameter provided, one available field should be set.')
            return u.User()

        if user is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User "{}" not found.'.format(request))
            return u.User()

        return user

    def CreateUser(self, request, context):
        # only create if user doesn't exist
        existing_user = self.storage.users.find_one({'email': request.email})
        if existing_user is None:
            user = u.User(name=request.name, email=request.email, password=request.password, available_effort=request.available_effort)
            result = self.storage.users.insert_one(self.storage.encode(user))
            return self.GetUser(u.GetUserRequest(_id=str(result.inserted_id)), context)
        else:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details('User "{}" already exists.'.format(request.email))
            return u.User()

    def UpdateUser(self, request, context):
        user_id = request._id
        if user_id:
            user_id = ObjectId(user_id)
            # only update if user exists
            existing_user = self.storage.users.find_one({'_id': user_id})
            if existing_user is not None:
                logging.info('UpdateUser, before update in dict: {}'.format(existing_user))
                existing_user = self.storage.decode(existing_user, u.User)
                existing_user.MergeFrom(request.user)
                logging.info('UpdateUser, merged Proto: {}'.format(existing_user))
                result = self.storage.users.replace_one(
                        {'_id': user_id},
                        self.storage.encode(existing_user)
                        )
                return self.GetUser(u.GetUserRequest(_id=request._id), context)
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('User id "{}" does not exist.'.format(user_id))
                return u.User()
        else:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('_id is mandatory'.format(user_id))
            return u.User()

    def DeleteUser(self, request, context):
        user_id = request._id
        if not isinstance(user_id, ObjectId):
            user_id = ObjectId(user_id)

        # only delete if user exists and we need to return the deleted user anyway
        existing_user = self.storage.users.find_one({'_id': user_id})
        if existing_user is not None:
            result = self.storage.users.delete_one({'_id': user_id})
            del existing_user['_id'] # delete id to signify the user doesn't exist
            return self.storage.decode(existing_user, u.User)
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

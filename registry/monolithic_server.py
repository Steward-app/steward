from concurrent import futures
from absl import logging, flags, app

import grpc
from grpc_reflection.v1alpha import reflection

from steward import user_pb2 as u
from steward import maintenance_pb2 as m
from steward import registry_pb2_grpc, registry_pb2
from registry import server_flags, user_server, maintenance_server, storage

FLAGS = flags.FLAGS

#flags.DEFINE_string('listen_addr', '[::]:50051', 'Address to listen.')

def serve(argv):
    s = storage.StorageManager()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    registry_pb2_grpc.add_UserServiceServicer_to_server(user_server.UserServiceServicer(storage_manager=s), server)
    registry_pb2_grpc.add_MaintenanceServiceServicer_to_server(maintenance_server.MaintenanceServiceServicer(storage_manager=s), server)
    SERVICE_NAMES = (
            registry_pb2.DESCRIPTOR.services_by_name['UserService'].full_name,
            registry_pb2.DESCRIPTOR.services_by_name['MaintenanceService'].full_name,
            reflection.SERVICE_NAME,
            )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port(FLAGS.listen_addr)
    logging.info('Monolithic Server listening to: {0}'.format(FLAGS.listen_addr))
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    app.run(serve)

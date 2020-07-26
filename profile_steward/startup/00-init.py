import grpc, os
from absl import logging, flags
from steward import user_pb2 as u
from steward import maintenance_pb2 as m
from steward import asset_pb2 as a
from steward import registry_pb2_grpc

FLAGS = flags.FLAGS

from registry import storage

if 'STEWARD_DB' in os.environ:
    FLAGS.db = os.environ['STEWARD_DB']

channel = grpc.insecure_channel('localhost:50051')
users = registry_pb2_grpc.UserServiceStub(channel)
maintenances = registry_pb2_grpc.MaintenanceServiceStub(channel)
assets = registry_pb2_grpc.AssetServiceStub(channel)

flags.FLAGS.mark_as_parsed()
stor = storage.StorageManager()

print('Available objects: stor')
print('Available protos: u, m, a')

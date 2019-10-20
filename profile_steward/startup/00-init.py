import grpc
from steward import user_pb2 as u
from steward import maintenance_pb2 as m
from steward import registry_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
users = registry_pb2_grpc.UserServiceStub(channel)
maintenances = registry_pb2_grpc.MaintenanceServiceStub(channel)

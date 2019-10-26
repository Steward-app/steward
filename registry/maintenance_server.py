from concurrent import futures
from absl import logging, flags, app

import grpc
from grpc_reflection.v1alpha import reflection

from bson.objectid import ObjectId

from registry import storage, server_flags

from steward import maintenance_pb2 as m
from steward import registry_pb2_grpc, registry_pb2


FLAGS = flags.FLAGS


class MaintenanceServiceServicer(registry_pb2_grpc.MaintenanceServiceServicer):
    def __init__(self, argv=None):
        self.storage = storage.StorageManager()
        logging.info('MaintenanceService initialized.')

    def GetMaintenance(self, request, context):
        maintenance_id = request._id
        if maintenance_id:
            maintenance_id = ObjectId(maintenance_id) # str -> ObjectId
            data_bson = self.storage.maintenances.find_one({'_id': maintenance_id})
        else:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('No search parameter provided, one available field should be set.')
            return m.Maintenance()

        if data_bson is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Maintenance "{}" not found.'.format(request))
            return m.Maintenance()

        return self.storage.decode(data_bson, m.Maintenance)

    def CreateMaintenance(self, request, context):
        # only create if maintenance doesn't exist
        existing_maintenance = self.storage.maintenances.find_one({'email': request.email})
        if existing_maintenance is None:
            maintenance = m.Maintenance(name=request.name, email=request.email, password=request.password, available_effort=request.available_effort)
            result = self.storage.maintenances.insert_one(self.storage.encode(maintenance))
            return self.GetMaintenance(m.GetMaintenanceRequest(_id=str(result.inserted_id)), context)
        else:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details('Maintenance "{}" already exists.'.format(request.email))
            return m.Maintenance()

    def UpdateMaintenance(self, request, context):
        maintenance_id = request._id
        if maintenance_id:
            maintenance_id = ObjectId(maintenance_id)
            # only update if maintenance exists
            existing_maintenance = self.storage.maintenances.find_one({'_id': maintenance_id})
            if existing_maintenance is not None:
                logging.info('UpdateMaintenance, before update in dict: {}'.format(existing_maintenance))
                existing_maintenance = self.storage.decode(existing_maintenance, m.Maintenance)
                existing_maintenance.MergeFrom(request.maintenance)
                logging.info('UpdateMaintenance, merged Proto: {}'.format(existing_maintenance))
                result = self.storage.maintenances.replace_one(
                        {'_id': maintenance_id},
                        self.storage.encode(existing_maintenance)
                        )
                return self.GetMaintenance(m.GetMaintenanceRequest(_id=request._id), context)
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('Maintenance id "{}" does not exist.'.format(maintenance_id))
                return m.Maintenance()
        else:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('_id is mandatory'.format(maintenance_id))
            return m.Maintenance()

    def DeleteMaintenance(self, request, context):
        maintenance_id = request._id
        if not isinstance(maintenance_id, ObjectId):
            maintenance_id = ObjectId(maintenance_id)

        # only delete if maintenance exists and we need to return the deleted maintenance anyway
        existing_maintenance = self.storage.maintenances.find_one({'_id': maintenance_id})
        if existing_maintenance is not None:
            result = self.storage.maintenances.delete_one({'_id': maintenance_id})
            del existing_maintenance['_id'] # delete id to signify the maintenance doesn't exist
            return self.storage.decode(existing_maintenance, m.Maintenance)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Maintenance id "{}" does not exist.'.format(maintenance_id))
            return m.Maintenance()

    def ListMaintenances(self, request, context):
        for maintenance_bson in self.storage.maintenances.find():
            maintenance = m.Maintenance()
            yield self.storage.decode(maintenance_bson, m.Maintenance)

def serve(argv):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    registry_pb2_grpc.add_MaintenanceServiceServicer_to_server(MaintenanceServiceServicer(), server)
    SERVICE_NAMES = (
            registry_pb2.DESCRIPTOR.services_by_name['MaintenanceService'].full_name,
            reflection.SERVICE_NAME,
            )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port(FLAGS.listen_addr)
    logging.info('Maintenance Microserver listening to: {0}'.format(FLAGS.listen_addr))
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    app.run(serve)

from concurrent import futures
from absl import logging, flags, app

import grpc
from grpc_reflection.v1alpha import reflection

from registry import storage, server_flags
from registry.decorators import must_have, must_have_any

from steward import maintenance_pb2 as m
from steward import registry_pb2_grpc, registry_pb2

FLAGS = flags.FLAGS

class MaintenanceServiceServicer(registry_pb2_grpc.MaintenanceServiceServicer):
    def __init__(self, storage_manager=None, argv=None):
        if not storage_manager:
            self.storage = storage.StorageManager()
        else:
            self.storage = storage_manager
        logging.info('MaintenanceService initialized.')

    @must_have('_id', m.Maintenance)
    def GetMaintenance(self, request, context):
        maintenance_id = request._id
        if maintenance_id:
            maintenance = self.storage.maintenances[maintenance_id]

        if maintenance == m.Maintenance():
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Maintenance "{}" not found.'.format(request))
            return m.Maintenance()

        return maintenance

    @must_have('name', m.Maintenance)
    @must_have('asset', m.Maintenance)
    def CreateMaintenance(self, request, context):
        logging.info('Creating maintenance from: {request}'.format(request=request))
        return self.storage.maintenances.new(request)

    @must_have('_id', m.Maintenance)
    @must_have('maintenance', m.Maintenance)
    def UpdateMaintenance(self, request, context):
        maintenance_id = request._id
        logging.info('UpdateMaintenance {}'.format(maintenance_id))
        # only update if maintenance exists
        maintenance = self.storage.maintenances[maintenance_id]
        if maintenance is not m.Maintenance(): # if not empty
            logging.info('UpdateMaintenance, before update in dict: {}'.format(maintenance))
            maintenance.MergeFrom(request.maintenance)
            logging.info('UpdateMaintenance, merged Proto: {}'.format(maintenance))
            result = self.storage.maintenances[maintenance_id] = maintenance
            return self.GetMaintenance(m.GetMaintenanceRequest(_id=maintenance_id), context)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Maintenance id "{}" does not exist.'.format(maintenance_id))
            return m.Maintenance()

    @must_have('_id', m.Maintenance)
    def DeleteMaintenance(self, request, context):
        maintenance_id = request._id

        # only delete if maintenance exists and we need to return the deleted maintenance anyway
        maintenance = self.storage.maintenances[maintenance_id]
        if maintenance != m.Maintenance():
            del self.storage.maintenances[maintenance_id]
            return maintenance
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Maintenance id "{}" does not exist.'.format(maintenance_id))
            return m.Maintenance()

    def ListMaintenances(self, request, context):
        for maintenance in self.storage.maintenances:
            yield maintenance

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

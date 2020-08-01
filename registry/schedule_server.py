from concurrent import futures
from absl import logging, flags, app
import sentry_sdk

import grpc
from grpc_reflection.v1alpha import reflection

from registry import storage, server_flags
from registry.decorators import must_have, must_have_any

from steward import schedule_pb2 as s
from steward import registry_pb2_grpc, registry_pb2

FLAGS = flags.FLAGS

class ScheduleServiceServicer(registry_pb2_grpc.ScheduleServiceServicer):
    def __init__(self, storage_manager=None, argv=None):
        if not storage_manager:
            self.storage = storage.StorageManager()
        else:
            self.storage = storage_manager
        logging.info('ScheduleService initialized.')

    @must_have('_id', s.Schedule)
    def GetSchedule(self, request, context):
        schedule_id = request._id
        if schedule_id:
            schedule = self.storage.schedules[schedule_id]

        if schedule == s.Schedule():
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Schedule "{}" not found.'.format(request))
            return s.Schedule()

        return schedule

    @must_have('description', s.Schedule)
    def CreateSchedule(self, request, context):
        logging.info('Creating schedule from: {request}'.format(request=request))
        return self.storage.schedules.new(request)

    @must_have('_id', s.Schedule)
    @must_have('schedule', s.Schedule)
    def UpdateSchedule(self, request, context):
        schedule_id = request._id
        logging.info('UpdateSchedule {}'.format(schedule_id))
        # only update if schedule exists
        schedule = self.storage.schedules[schedule_id]
        if schedule is not s.Schedule(): # if not empty
            logging.info('UpdateSchedule, before update in dict: {}'.format(schedule))
            schedule.MergeFrom(request.schedule)
            logging.info('UpdateSchedule, merged Proto: {}'.format(schedule))
            result = self.storage.schedules[schedule_id] = schedule
            return self.GetSchedule(s.GetScheduleRequest(_id=schedule_id), context)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Schedule id "{}" does not exist.'.format(schedule_id))
            return s.Schedule()

    @must_have('_id', s.Schedule)
    def DeleteSchedule(self, request, context):
        schedule_id = request._id

        # only delete if schedule exists and we need to return the deleted schedule anyway
        schedule = self.storage.schedules[schedule_id]
        if schedule != s.Schedule():
            del self.storage.schedules[schedule_id]
            return schedule
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Schedule id "{}" does not exist.'.format(schedule_id))
            return s.Schedule()

    def ListSchedules(self, request, context):
        for schedule in self.storage.schedules:
            yield schedule

def serve(argv):
    from registry.monitoring import psi
    if FLAGS.sentry:
        sentry_sdk.init(FLAGS.sentry)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=(psi,))
    registry_pb2_grpc.add_ScheduleServiceServicer_to_server(ScheduleServiceServicer(), server)
    SERVICE_NAMES = (
            registry_pb2.DESCRIPTOR.services_by_name['ScheduleService'].full_name,
            reflection.SERVICE_NAME,
            )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port(FLAGS.listen_addr)
    logging.info('Schedule Microserver listening to: {0}'.format(FLAGS.listen_addr))
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    app.run(serve)

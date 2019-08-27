# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: steward/maintenance.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from steward import asset_pb2 as steward_dot_asset__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='steward/maintenance.proto',
  package='steward',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x19steward/maintenance.proto\x12\x07steward\x1a\x1egoogle/protobuf/duration.proto\x1a\x13steward/asset.proto\"\x9b\x02\n\x0bMaintenance\x12\x0b\n\x03_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x1d\n\x05\x61sset\x18\x04 \x01(\x0b\x32\x0e.steward.Asset\x1aq\n\x08Schedule\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t\x12#\n\x04type\x18\x02 \x01(\x0e\x32\x15.steward.ScheduleType\x12+\n\x08interval\x18\x03 \x01(\x0b\x32\x19.google.protobuf.Duration\x1aJ\n\x06Snooze\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t\x12+\n\x08\x64uration\x18\x02 \x01(\x0b\x32\x19.google.protobuf.Duration**\n\x0cScheduleType\x12\x0c\n\x08\x44URATION\x10\x00\x12\x0c\n\x08\x45XTERNAL\x10\x01\x62\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_duration__pb2.DESCRIPTOR,steward_dot_asset__pb2.DESCRIPTOR,])

_SCHEDULETYPE = _descriptor.EnumDescriptor(
  name='ScheduleType',
  full_name='steward.ScheduleType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DURATION', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EXTERNAL', index=1, number=1,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=377,
  serialized_end=419,
)
_sym_db.RegisterEnumDescriptor(_SCHEDULETYPE)

ScheduleType = enum_type_wrapper.EnumTypeWrapper(_SCHEDULETYPE)
DURATION = 0
EXTERNAL = 1



_MAINTENANCE_SCHEDULE = _descriptor.Descriptor(
  name='Schedule',
  full_name='steward.Maintenance.Schedule',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='description', full_name='steward.Maintenance.Schedule.description', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='steward.Maintenance.Schedule.type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='interval', full_name='steward.Maintenance.Schedule.interval', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=186,
  serialized_end=299,
)

_MAINTENANCE_SNOOZE = _descriptor.Descriptor(
  name='Snooze',
  full_name='steward.Maintenance.Snooze',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='description', full_name='steward.Maintenance.Snooze.description', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='duration', full_name='steward.Maintenance.Snooze.duration', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=301,
  serialized_end=375,
)

_MAINTENANCE = _descriptor.Descriptor(
  name='Maintenance',
  full_name='steward.Maintenance',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='_id', full_name='steward.Maintenance._id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='steward.Maintenance.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='steward.Maintenance.description', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='asset', full_name='steward.Maintenance.asset', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_MAINTENANCE_SCHEDULE, _MAINTENANCE_SNOOZE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=92,
  serialized_end=375,
)

_MAINTENANCE_SCHEDULE.fields_by_name['type'].enum_type = _SCHEDULETYPE
_MAINTENANCE_SCHEDULE.fields_by_name['interval'].message_type = google_dot_protobuf_dot_duration__pb2._DURATION
_MAINTENANCE_SCHEDULE.containing_type = _MAINTENANCE
_MAINTENANCE_SNOOZE.fields_by_name['duration'].message_type = google_dot_protobuf_dot_duration__pb2._DURATION
_MAINTENANCE_SNOOZE.containing_type = _MAINTENANCE
_MAINTENANCE.fields_by_name['asset'].message_type = steward_dot_asset__pb2._ASSET
DESCRIPTOR.message_types_by_name['Maintenance'] = _MAINTENANCE
DESCRIPTOR.enum_types_by_name['ScheduleType'] = _SCHEDULETYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Maintenance = _reflection.GeneratedProtocolMessageType('Maintenance', (_message.Message,), {

  'Schedule' : _reflection.GeneratedProtocolMessageType('Schedule', (_message.Message,), {
    'DESCRIPTOR' : _MAINTENANCE_SCHEDULE,
    '__module__' : 'steward.maintenance_pb2'
    # @@protoc_insertion_point(class_scope:steward.Maintenance.Schedule)
    })
  ,

  'Snooze' : _reflection.GeneratedProtocolMessageType('Snooze', (_message.Message,), {
    'DESCRIPTOR' : _MAINTENANCE_SNOOZE,
    '__module__' : 'steward.maintenance_pb2'
    # @@protoc_insertion_point(class_scope:steward.Maintenance.Snooze)
    })
  ,
  'DESCRIPTOR' : _MAINTENANCE,
  '__module__' : 'steward.maintenance_pb2'
  # @@protoc_insertion_point(class_scope:steward.Maintenance)
  })
_sym_db.RegisterMessage(Maintenance)
_sym_db.RegisterMessage(Maintenance.Schedule)
_sym_db.RegisterMessage(Maintenance.Snooze)


# @@protoc_insertion_point(module_scope)
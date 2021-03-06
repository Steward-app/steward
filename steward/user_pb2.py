# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/steward/user.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from proto.steward import organization_pb2 as proto_dot_steward_dot_organization__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='proto/steward/user.proto',
  package='steward',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x18proto/steward/user.proto\x12\x07steward\x1a proto/steward/organization.proto\"u\n\x04User\x12\x0b\n\x03_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08password\x18\x03 \x01(\t\x12\r\n\x05\x65mail\x18\x04 \x01(\t\x12\x18\n\x10\x61vailable_effort\x18\x05 \x01(\x02\x12\x17\n\x0forganization_id\x18\x06 \x01(\t\"\x7f\n\x03\x41\x43L\x12\x0b\n\x03_id\x18\x01 \x01(\t\x12\x1b\n\x04user\x18\x02 \x01(\x0b\x32\r.steward.User\x12+\n\x0corganization\x18\x03 \x01(\x0b\x32\x15.steward.Organization\x12!\n\x05level\x18\x04 \x01(\x0e\x32\x12.steward.UserLevel\",\n\x0eGetUserRequest\x12\x0b\n\x03_id\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\" \n\x11\x44\x65leteUserRequest\x12\x0b\n\x03_id\x18\x01 \x01(\t\"=\n\x11UpdateUserRequest\x12\x0b\n\x03_id\x18\x01 \x01(\t\x12\x1b\n\x04user\x18\x02 \x01(\x0b\x32\r.steward.User\"\x12\n\x10ListUsersRequest\"u\n\x11\x43reateUserRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\r\n\x05\x65mail\x18\x03 \x01(\t\x12\x18\n\x10\x61vailable_effort\x18\x04 \x01(\x02\x12\x17\n\x0forganization_id\x18\x05 \x01(\t*/\n\tUserLevel\x12\r\n\tANONYMOUS\x10\x00\x12\x08\n\x04USER\x10\x01\x12\t\n\x05OWNER\x10\x02\x62\x06proto3'
  ,
  dependencies=[proto_dot_steward_dot_organization__pb2.DESCRIPTOR,])

_USERLEVEL = _descriptor.EnumDescriptor(
  name='UserLevel',
  full_name='steward.UserLevel',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ANONYMOUS', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='USER', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='OWNER', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=601,
  serialized_end=648,
)
_sym_db.RegisterEnumDescriptor(_USERLEVEL)

UserLevel = enum_type_wrapper.EnumTypeWrapper(_USERLEVEL)
ANONYMOUS = 0
USER = 1
OWNER = 2



_USER = _descriptor.Descriptor(
  name='User',
  full_name='steward.User',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='_id', full_name='steward.User._id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='steward.User.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='password', full_name='steward.User.password', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='email', full_name='steward.User.email', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='available_effort', full_name='steward.User.available_effort', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='organization_id', full_name='steward.User.organization_id', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=71,
  serialized_end=188,
)


_ACL = _descriptor.Descriptor(
  name='ACL',
  full_name='steward.ACL',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='_id', full_name='steward.ACL._id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user', full_name='steward.ACL.user', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='organization', full_name='steward.ACL.organization', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='level', full_name='steward.ACL.level', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=190,
  serialized_end=317,
)


_GETUSERREQUEST = _descriptor.Descriptor(
  name='GetUserRequest',
  full_name='steward.GetUserRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='_id', full_name='steward.GetUserRequest._id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='email', full_name='steward.GetUserRequest.email', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=319,
  serialized_end=363,
)


_DELETEUSERREQUEST = _descriptor.Descriptor(
  name='DeleteUserRequest',
  full_name='steward.DeleteUserRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='_id', full_name='steward.DeleteUserRequest._id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=365,
  serialized_end=397,
)


_UPDATEUSERREQUEST = _descriptor.Descriptor(
  name='UpdateUserRequest',
  full_name='steward.UpdateUserRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='_id', full_name='steward.UpdateUserRequest._id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user', full_name='steward.UpdateUserRequest.user', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=399,
  serialized_end=460,
)


_LISTUSERSREQUEST = _descriptor.Descriptor(
  name='ListUsersRequest',
  full_name='steward.ListUsersRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
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
  serialized_start=462,
  serialized_end=480,
)


_CREATEUSERREQUEST = _descriptor.Descriptor(
  name='CreateUserRequest',
  full_name='steward.CreateUserRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='steward.CreateUserRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='password', full_name='steward.CreateUserRequest.password', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='email', full_name='steward.CreateUserRequest.email', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='available_effort', full_name='steward.CreateUserRequest.available_effort', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='organization_id', full_name='steward.CreateUserRequest.organization_id', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=482,
  serialized_end=599,
)

_ACL.fields_by_name['user'].message_type = _USER
_ACL.fields_by_name['organization'].message_type = proto_dot_steward_dot_organization__pb2._ORGANIZATION
_ACL.fields_by_name['level'].enum_type = _USERLEVEL
_UPDATEUSERREQUEST.fields_by_name['user'].message_type = _USER
DESCRIPTOR.message_types_by_name['User'] = _USER
DESCRIPTOR.message_types_by_name['ACL'] = _ACL
DESCRIPTOR.message_types_by_name['GetUserRequest'] = _GETUSERREQUEST
DESCRIPTOR.message_types_by_name['DeleteUserRequest'] = _DELETEUSERREQUEST
DESCRIPTOR.message_types_by_name['UpdateUserRequest'] = _UPDATEUSERREQUEST
DESCRIPTOR.message_types_by_name['ListUsersRequest'] = _LISTUSERSREQUEST
DESCRIPTOR.message_types_by_name['CreateUserRequest'] = _CREATEUSERREQUEST
DESCRIPTOR.enum_types_by_name['UserLevel'] = _USERLEVEL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

User = _reflection.GeneratedProtocolMessageType('User', (_message.Message,), {
  'DESCRIPTOR' : _USER,
  '__module__' : 'proto.steward.user_pb2'
  # @@protoc_insertion_point(class_scope:steward.User)
  })
_sym_db.RegisterMessage(User)

ACL = _reflection.GeneratedProtocolMessageType('ACL', (_message.Message,), {
  'DESCRIPTOR' : _ACL,
  '__module__' : 'proto.steward.user_pb2'
  # @@protoc_insertion_point(class_scope:steward.ACL)
  })
_sym_db.RegisterMessage(ACL)

GetUserRequest = _reflection.GeneratedProtocolMessageType('GetUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETUSERREQUEST,
  '__module__' : 'proto.steward.user_pb2'
  # @@protoc_insertion_point(class_scope:steward.GetUserRequest)
  })
_sym_db.RegisterMessage(GetUserRequest)

DeleteUserRequest = _reflection.GeneratedProtocolMessageType('DeleteUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETEUSERREQUEST,
  '__module__' : 'proto.steward.user_pb2'
  # @@protoc_insertion_point(class_scope:steward.DeleteUserRequest)
  })
_sym_db.RegisterMessage(DeleteUserRequest)

UpdateUserRequest = _reflection.GeneratedProtocolMessageType('UpdateUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _UPDATEUSERREQUEST,
  '__module__' : 'proto.steward.user_pb2'
  # @@protoc_insertion_point(class_scope:steward.UpdateUserRequest)
  })
_sym_db.RegisterMessage(UpdateUserRequest)

ListUsersRequest = _reflection.GeneratedProtocolMessageType('ListUsersRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTUSERSREQUEST,
  '__module__' : 'proto.steward.user_pb2'
  # @@protoc_insertion_point(class_scope:steward.ListUsersRequest)
  })
_sym_db.RegisterMessage(ListUsersRequest)

CreateUserRequest = _reflection.GeneratedProtocolMessageType('CreateUserRequest', (_message.Message,), {
  'DESCRIPTOR' : _CREATEUSERREQUEST,
  '__module__' : 'proto.steward.user_pb2'
  # @@protoc_insertion_point(class_scope:steward.CreateUserRequest)
  })
_sym_db.RegisterMessage(CreateUserRequest)


# @@protoc_insertion_point(module_scope)

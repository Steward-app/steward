import pytest
import grpc
from registry import storage, user_server


from pprint import pprint

from steward.user_pb2 import User, GetUserRequest, CreateUserRequest, DeleteUserRequest, UpdateUserRequest

@pytest.fixture(scope='module')
def grpc_add_to_server():
    from steward.registry_pb2_grpc import add_UserServiceServicer_to_server
    return add_UserServiceServicer_to_server

@pytest.fixture(scope='module')
def grpc_servicer():
    from absl import flags, app
    import sys
    FLAGS = flags.FLAGS
    FLAGS(sys.argv)
    FLAGS.env = 'testing'
    from registry.user_server import UserServiceServicer
    return UserServiceServicer()

@pytest.fixture(scope='module')
def grpc_stub_cls(grpc_channel):
    from steward.registry_pb2_grpc import UserServiceStub
    return UserServiceStub




def test_GetUser_errors(grpc_stub):
    request = GetUserRequest()

    with pytest.raises(grpc.RpcError) as e:
        response = grpc_stub.GetUser(request)
    assert e.value.code() == grpc.StatusCode.INVALID_ARGUMENT

    request.email = 'doesNotExist'
    with pytest.raises(grpc.RpcError) as e:
        response = grpc_stub.GetUser(request)
    assert e.value.code() == grpc.StatusCode.NOT_FOUND


def test_CreateUpdateDeleteUser(grpc_stub):
    import time
    test_id = str(time.time())

    # Create
    request = CreateUserRequest(name='PyTest', email='pytest+'+ test_id +'@example.com', password='hunter2', available_effort=0.8)
    created_user = grpc_stub.CreateUser(request)
    inserted_id = created_user._id

    print(created_user)

    with pytest.raises(grpc.RpcError) as e:
        duplicate_response = grpc_stub.CreateUser(request)
    assert e.value.code() == grpc.StatusCode.ALREADY_EXISTS

    # Update
    request = UpdateUserRequest(_id=inserted_id, user=User(name='KillMe'))
    updated_user = grpc_stub.UpdateUser(request)

    print(updated_user)
    assert updated_user.name == 'KillMe'
    updated_user = grpc_stub.GetUser(GetUserRequest(_id=inserted_id))
    print(updated_user)
    # Delete
    request = DeleteUserRequest(_id=inserted_id)
    del_response = grpc_stub.DeleteUser(request)

    with pytest.raises(grpc.RpcError) as e:
        response = grpc_stub.GetUser(GetUserRequest(_id=inserted_id))
    assert e.value.code() == grpc.StatusCode.NOT_FOUND

import pytest
import grpc

from pprint import pprint

from steward.user_pb2 import User, GetUserRequest, CreateUserRequest

@pytest.fixture(scope='module')
def grpc_add_to_server():
    from steward.registry_pb2_grpc import add_UserServiceServicer_to_server
    return add_UserServiceServicer_to_server

@pytest.fixture(scope='module')
def grpc_servicer():
    from registry.user_server import UserServiceServicer
    return UserServiceServicer(env='pytest')

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

def test_CreateUser(grpc_stub):
    request = CreateUserRequest(name='PyTest', email='pytest@example.com', password='hunter2', available_effort=0.8)
    response = grpc_stub.CreateUser(request)

    with pytest.raises(grpc.RpcError) as e:
        response = grpc_stub.CreateUser(request)
    assert e.value.code() == grpc.StatusCode.ALREADY_EXISTS

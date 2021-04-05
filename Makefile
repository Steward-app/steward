PROTO_OUT = steward
PROTO_IN = proto/proto/steward
PROTO_INCLUDE = proto
PROTO_MOVE = proto/steward

.PHONY: requirements proto clean

all: requirements proto

requirements:
	poetry install

proto:
	rm -rf $(PROTO_OUT)
	poetry run python -m grpc_tools.protoc -I $(PROTO_INCLUDE) --python_out=. --grpc_python_out=. $(PROTO_IN)/*.proto
	mv $(PROTO_MOVE) $(PROTO_OUT)

clean:
	rm  -rf $(PROTO_OUT)

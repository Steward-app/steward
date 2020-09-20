PROTO_OUT = steward
PROTO_IN = proto/proto/steward
PROTO_INCLUDE = proto
PROTO_MOVE = proto/steward

.PHONY: requirements proto clean

all: requirements proto

requirements:
	python3 -m pip install -r requirements.txt

proto:
	rm -rf $(PROTO_OUT)
	python3 -m grpc_tools.protoc -I $(PROTO_INCLUDE) --python_out=. --grpc_python_out=. $(PROTO_IN)/*.proto
	mv $(PROTO_MOVE) $(PROTO_OUT)

clean:
	rm  -rf app/$(NODE_MODULES) $(PROTO_OUT)

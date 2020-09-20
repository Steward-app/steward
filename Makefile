PROTO_OUT = steward
PROTO_IN = proto/steward
PROTO_INCLUDE = proto

.PHONY: requirements proto clean

requirements:
	python3 -m pip install -r requirements.txt

proto: requirements
	rm -rf $(PROTO_OUT)/*.py
	rm -rf $(PROTO_OUT)/__pycache__
	python3 -m grpc_tools.protoc -I $(PROTO_INCLUDE) --python_out=. --grpc_python_out=. $(PROTO_IN)/*.proto

clean:
	rm  -rf app/$(NODE_MODULES) $(PROTO_OUT)

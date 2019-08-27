#!/bin/sh
rm -r steward/*.py
python3 -m grpc_tools.protoc -I proto --python_out=. --grpc_python_out=. proto/steward/*.proto

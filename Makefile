# You can set these variables from the command line.
NODE_MODULES = static/node_modules
PROTO_OUT = steward
PROTO_IN = proto/steward
PROTO_INCLUDE = proto

dependencies:
	sudo pip3 install -r requirements.txt

.PHONY: app
app:
	cd app; yarn install --modules-folder $(NODE_MODULES)
	cd app; FLASK_APP=__init__.py flask assets build

.PHONY: proto
proto:
	rm -rf $(PROTO_OUT)/*.py
	rm -rf $(PROTO_OUT)/__pycache__
	python3 -m grpc_tools.protoc -I $(PROTO_INCLUDE) --python_out=. --grpc_python_out=. $(PROTO_IN)/*.proto

clean:
	rm  -rf app/$(NODE_MODULES) $(PROTO_OUT)

run_backend:
	python3 -m registry.user_server --env dev

run_frontend:
	python3 -c 'from app import app; app.run(host="0.0.0.0", port=5000)'

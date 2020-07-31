# You can set these variables from the command line.
NODE_MODULES = static/node_modules
PROTO_OUT = steward
PROTO_IN = proto/steward
PROTO_INCLUDE = proto
BACKENDS = registry.user_server registry.maintenance_server registry.asset_server registry.schedule_server
BE_ARGS = --env dev --logtostderr --db=mongodb://127.0.0.1:27017
FE_PORT = 5000

dependencies:
	sudo pip3 install -r requirements.txt

.PHONY: app proto clean run_backend $(BACKENDS) run_frontend run_backend_monolithic registry.monolithic_server
app:
	cd app; yarn install --modules-folder $(NODE_MODULES)
	cd app; FLASK_APP=__init__.py flask assets build

proto:
	rm -rf $(PROTO_OUT)/*.py
	rm -rf $(PROTO_OUT)/__pycache__
	python3 -m grpc_tools.protoc -I $(PROTO_INCLUDE) --python_out=. --grpc_python_out=. $(PROTO_IN)/*.proto

clean:
	rm  -rf app/$(NODE_MODULES) $(PROTO_OUT)

run_backend: $(BACKENDS)

run_backend_monolithic: registry.monolithic_server

registry.monolithic_server:
	python3 -m $@ $(BE_ARGS) $(ARGS) --listen_addr '[::]:50050'

registry.user_server:
	python3 -m $@ $(BE_ARGS) $(ARGS) --listen_addr '[::]:50051'

registry.maintenance_server:
	python3 -m $@ $(BE_ARGS) $(ARGS) --listen_addr '[::]:50052'

registry.asset_server:
	python3 -m $@ $(BE_ARGS) $(ARGS) --listen_addr '[::]:50053'

registry.schedule_server:
	python3 -m $@ $(BE_ARGS) $(ARGS) --listen_addr '[::]:50054'

run_frontend:
	flask run -h 0.0.0.0

run_frontend_monolithic:
	python3 -c 'from app import app; app.run(host="0.0.0.0", load_dotenv=False, port=$(FE_PORT))'

test:
	python3 -m pytest

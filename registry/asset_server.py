from concurrent import futures
from absl import logging, flags, app
import sentry_sdk

import grpc
from grpc_reflection.v1alpha import reflection

from registry import storage, server_flags
from registry.decorators import must_have, must_have_any

from steward import asset_pb2 as a
from steward import registry_pb2_grpc, registry_pb2

FLAGS = flags.FLAGS

class AssetServiceServicer(registry_pb2_grpc.AssetServiceServicer):
    def __init__(self, storage_manager=None, argv=None):
        if not storage_manager:
            self.storage = storage.StorageManager()
        else:
            self.storage = storage_manager
        logging.info('AssetService initialized.')

    @must_have('_id', a.Asset)
    def GetAsset(self, request, context):
        asset_id = request._id
        if asset_id:
            asset = self.storage.assets[asset_id]

        if asset == a.Asset():
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Asset "{}" not found.'.format(request))
            return a.Asset()

        return asset

    @must_have('name', a.Asset)
    def CreateAsset(self, request, context):
        logging.info('Creating asset from: {request}'.format(request=request))
        return self.storage.assets.new(request)

    @must_have('_id', a.Asset)
    def UpdateAsset(self, request, context):
        asset_id = request._id
        logging.info('UpdateAsset {}'.format(asset_id))
        # only update if asset exists
        asset = self.storage.assets[asset_id]
        if asset is not a.Asset(): # if not empty
            logging.info('UpdateAsset, before update in dict: {}'.format(asset))
            asset.MergeFrom(request.asset)
            logging.info('UpdateAsset, merged Proto: {}'.format(asset))
            result = self.storage.assets[asset_id] = asset
            return self.GetAsset(a.GetAssetRequest(_id=asset_id), context)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Asset id "{}" does not exist.'.format(asset_id))
            return a.Asset()

    @must_have('_id', a.Asset)
    def DeleteAsset(self, request, context):
        asset_id = request._id

        # only delete if asset exists and we need to return the deleted asset anyway
        asset = self.storage.assets[asset_id]
        if asset != a.Asset():
            del self.storage.assets[asset_id]
            asset._id = ''
            return asset
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Asset id "{}" does not exist.'.format(asset_id))
            return a.Asset()

    def ListAssets(self, request, context):
        for asset in self.storage.assets:
            yield asset

def serve(argv):
    if FLAGS.sentry:
        sentry_sdk.init(FLAGS.sentry)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    registry_pb2_grpc.add_AssetServiceServicer_to_server(AssetServiceServicer(), server)
    SERVICE_NAMES = (
            registry_pb2.DESCRIPTOR.services_by_name['AssetService'].full_name,
            reflection.SERVICE_NAME,
            )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    server.add_insecure_port(FLAGS.listen_addr)
    logging.info('Asset Microserver listening to: {0}'.format(FLAGS.listen_addr))
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    app.run(serve)

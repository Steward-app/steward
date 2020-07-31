from absl import logging
import os
USER_ENDPOINT = os.environ.get('USER_ENDPOINT') or 'localhost:50050'
MAINTENANCE_ENDPOINT = os.environ.get('MAINTENANCE_ENDPOINT') or 'localhost:50050'
ASSET_ENDPOINT = os.environ.get('ASSET_ENDPOINT') or 'localhost:50050'
SCHEDULE_ENDPOINT = os.environ.get('SCHEDULE_ENDPOINT') or 'localhost:50050'
del os

logging.info('Initialized channels:\n user_server: {user}\n maintenance_server: {maintenance}\n asset_server: {asset}\n schedule_server: {schedule}'.format(
    user=USER_ENDPOINT,
    maintenance=MAINTENANCE_ENDPOINT,
    asset=ASSET_ENDPOINT,
    schedule=SCHEDULE_ENDPOINT
    ))

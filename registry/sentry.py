from absl import logging
import sentry_sdk

def init(dsn):
    if dsn:
        try:
            sentry_sdk.init(dsn)
        except:
            logging.error('Failed to init DSN: {dsn}'.format(dsn=dsn))
        else:
            logging.info('Initialized Sentry DSN: {dsn}'.format(dsn=dsn))

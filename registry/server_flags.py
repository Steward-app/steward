from absl import logging, flags

FLAGS = flags.FLAGS

flags.DEFINE_string('listen_addr', '[::]:50051', 'Address to listen.')
flags.DEFINE_string('sentry', None, 'Sentry endpoint')

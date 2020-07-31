from absl import logging, flags

FLAGS = flags.FLAGS

flags.DEFINE_string('listen_addr', '[::]:50050', 'Address to listen.')
flags.DEFINE_string('sentry', None, 'Sentry endpoint')

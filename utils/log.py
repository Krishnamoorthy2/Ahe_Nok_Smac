import logging
# from features.info import logPath


class logInfo():

	def __init__(self, act):
		self.msg = "init message"

		self.logger = logging.getLogger(act)
		self.logger.setLevel(logging.DEBUG)

		fh = logging.FileHandler(
			"/home/smacar/work/snappon_core/log/engine.log")
		fh.setLevel(logging.DEBUG)

		self._formatter = logging.Formatter(
			'%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		fh.setFormatter(self._formatter)

		self.logger.addHandler(fh)

	def dump(self, lvl, msg):
		self.msg = msg

		if lvl == 0:
			self.logger.debug(self.msg)
		elif lvl == 1:
			self.logger.info(self.msg)
		elif lvl == 2:
			self.logger.warn(self.msg)
		elif lvl == 3:
			self.logger.error(self.msg)
		elif lvl == 4:
			self.logger.critical(self.msg)


# from log.log import logInfo
# action = "[RECONSTRUCT]"
# log = logInfo(action)
# log.dump(1, "SUCCESS")
# log.dump(3, e)


# import logging

# logger = logging.getLogger('simple_example')
# logger.setLevel(logging.DEBUG)
# # create file handler that logs debug and higher level messages
# fh = logging.FileHandler('spam.log')
# fh.setLevel(logging.DEBUG)
# # create console handler with a higher log level
# ch = logging.StreamHandler()
# ch.setLevel(logging.ERROR)
# # create formatter and add it to the handlers
# formatter = logging.Formatter(
#     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# fh.setFormatter(formatter)
# # add the handlers to logger
# logger.addHandler(ch)
# logger.addHandler(fh)

# # 'application' code
# logger.debug('debug message')
# logger.info('info message')
# logger.warn('warn message')
# logger.error('error message')
# logger.critical('critical message')

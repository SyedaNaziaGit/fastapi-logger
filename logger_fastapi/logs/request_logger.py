from logs.logger_config import request_id_variable, baseLogger
class RequestLogger:
    def __init__(self, logger):
        self._logger = logger

    def _inject_request_id(self, message):
        req_id = request_id_variable.get()
        if isinstance(message, dict):
            message["request_id"] = req_id
        else:
            message = {"message": message, "request_id": req_id}
        return message

    def debug(self, message, *args, **kwargs):
        self._logger.debug(self._inject_request_id(message), *args, **kwargs)

    def info(self, message, *args, **kwargs):
        self._logger.info(self._inject_request_id(message), *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self._logger.warning(self._inject_request_id(message), *args, **kwargs)

    def error(self, message, *args, **kwargs):
        self._logger.error(self._inject_request_id(message), *args, **kwargs)

    def exception(self, message, *args, **kwargs):
        self._logger.exception(self._inject_request_id(message), *args, **kwargs)


#logger instance
logger = RequestLogger(baseLogger)
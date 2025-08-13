from datetime import datetime,timezone
from pythonjsonlogger import jsonlogger
from logs.logger_config import SERVICE_NAME,ENV
#Customized UTC formatter class
class UTCFormatter(jsonlogger.JsonFormatter):
    def formatTime(self,record,datefmt = None):
        return datetime.fromtimestamp(record.created,tz =timezone.utc).isoformat()

#JSON Formatter - customize to add service and env
class CustJsonFormatter(UTCFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record["service"] = SERVICE_NAME
        log_record["environmrnt"] = ENV
        
#using loggong and RotatingFileHandler
import logging
from logging.handlers import RotatingFileHandler
import sys
from pathlib import Path
from pythonjsonlogger import  jsonlogger
import contextvars
import os
from logs.formatter import CustJsonFormatter

#Configuration
SERVICE_NAME = os.getenv("SERVICE_NAME","fastapi_logservice")
#Reading Environment variables
ENV = os.getenv("ENV","local") #local or prod environment

#Context variable to store requestID
request_id_variable =  contextvars.ContextVar("request_id",default= None)


#log format
#LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

#using JSON log formatter
jsonFormatter = jsonlogger.JsonFormatter(fmt="%(asctime)s %(name)s %(levelname)s %(message)s %(pathname)s %(lineno)d",datefmt="%Y-%m-%d %H:%M:%S")

#Creating Logger
baseLogger = logging.getLogger("fastapiLogger")
baseLogger.setLevel(logging.DEBUG)

if ENV == "local":
    #log files with rotation to local env
    #creating logs directory
    LOG_DIR = Path("logs")
    LOG_DIR.mkdir(exist_ok=True)
    #creating seperate error logs and information logs
    LOG_FILE_INFO = LOG_DIR/"app_info.json"
    LOG_FILE_ERROR = LOG_DIR/"app_error.json"
    #Logfile
    #LOG_FILE = LOG_DIR/"app.log"

    #Seperating File Handler into Information Handler and Error Handler

    #Information file handler
    infoHandler = RotatingFileHandler(LOG_FILE_INFO,maxBytes=5*1024*1024,backupCount=2)
    infoHandler.setLevel(logging.INFO)
    infoHandler.setFormatter(CustJsonFormatter)

    #Error file handler
    errorHandler = RotatingFileHandler(LOG_FILE_ERROR,maxBytes=5*1024*1024,backupCount=2)
    errorHandler.setLevel(logging.ERROR)
    errorHandler.setFormatter(CustJsonFormatter)

    #console
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setLevel(logging.INFO)
    #consoleHandler.setFormatter(logging.Formatter(LOG_FORMAT))
    consoleHandler.setFormatter(logging.Formatter(CustJsonFormatter))

    #Attaching handlers if not already added
    if not baseLogger.handlers:
        baseLogger.addHandler(infoHandler)
        baseLogger.addHandler(errorHandler)
        baseLogger.addHandler(consoleHandler)
else:
    #Prod environment - log info to stdout, err to stderr
    stdoutHandler = logging.StreamHandler(sys.stdout)
    stdoutHandler.setLevel(logging.INFO)
    stdoutHandler.setFormatter(CustJsonFormatter)
    
    stderrHandler = logging.StreamHandler(sys.stderr)
    stderrHandler.setFormatter(logging.ERROR)
    stderrHandler.setFormatter(CustJsonFormatter)
    
    if not  baseLogger.handlers:
        baseLogger.addHandler(stdoutHandler)
        baseLogger.addHandler(stderrHandler)
'''
#File handler along with roatation- here keeping 2 backups and 5MB per file
fileHandler = RotatingFileHandler(LOG_FILE,maxBytes=5*1024*1024,backupCount=2)
fileHandler.setLevel(logging.DEBUG)
#fileHandler.setFormatter(logging.Formatter(LOG_FORMAT))
fileHandler.setFormatter(logging.Formatter(jsonFormatter))
'''





    

from fastapi import FastAPI, HTTPException, Request,Depends
from pydantic import BaseModel
from logs.logger_config import logger
import time
import uuid
from logs.logger_config import request_id_variable
from logs.request_logger import logger

app = FastAPI()

#creating a middleware for  logging  requests and response
@app.middleware("http")
#async def  logRequests(request:Request,call_next):
async def addRequestID_middleware(request:Request,call_next):
    #generating the request id
    requestID = request.headers.get("X-Request-ID",str(uuid.uuid4()))
    request_id_variable.set(requestID)
    #request.state.request_id = requestID
    
    #tracking process time
    startTime = time.time()
    
    #logger.info(f"Incoming Request:{request.method} - {request.url}")
    logger.info({
        "event": "Incoming Request",
        "request_id" :requestID,
        "method" : request.method,
        "url":str(request.url)
    })
    try:
        response = await  call_next(request)
    except Exception as e:
        #logger.exception("Unhandled Exception")
        logger.exception({
            "event":"Unhandled exception",
            "request_id":requestID,
            "err":str(e)
        })
        raise e
    processTime = (time.time() - startTime)*1000
    #logger.info(f"Completed the process in {processTime:2f}ms - Status : {response.status_code}")
    logger.info({
        "event": "request_completed",
        "request_id":requestID,
        "status_code": response.status_code,
        "duration_ms": round(processTime, 2)
    })
    #returning response with X-Request-ID  header
    response.headers["X-Requset-ID"] = requestID
    return response

def getLogger():
    return logger

#Routes Here
@app.get("/hello")
def hello(log = Depends(getLogger)):
    #logger.debug("Inside /hello route")
    logger.debug({"event": "inside_route", "route": "/hello"})
    return {"messgae":"Logging Functionality Using FastAPI"}

@app.get("/error")
def throw_error(log = Depends(getLogger)):
    #logger.warning("This route will throw error")
    logger.warning({"event": "Raising an error functionality"})
    raise ValueError("Raising an error functionality")

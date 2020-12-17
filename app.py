#!/usr/bin/env python
 
import datetime, time, json, os, sys, subprocess, threading, socket, traceback
from pprint import pprint
 
# non default imports
from fastapi import FastAPI # pip install fastapi
import uvicorn # pip install uvicorn
 
APP_PORT = os.getenv('APP_PORT', 9999)
_PWD = os.getenv('PWD', "CHANGEME!")
 
app = FastAPI()
 
APP_NAME="gcti:mlcmd:api"
__version__ = "12.2020"
 
 
def get_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
 
def get_now_utc():
    return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
 
def get_now_utc_iso():
    return datetime.datetime.utcnow().isoformat()
 
def get_epoch():
    return time.time()
 
def get_epoch_nanoseconds():
    return time.time_ns()
 
def get_pid():
    return os.getpid()
 
def get_hostname():
    return socket.gethostname()
 
def get_appname():
    return APP_NAME
 
def get_app_uptime():
    secs = get_epoch() - app_start_time
    result = datetime.timedelta(seconds=secs)
    return str(result)
 
def dd(data, level="INFO", **kwargs):
    log = {'timestamp': get_now(), 'epoch': get_epoch(), 'pid': get_pid(), 'level': level, 'message': data}
    if kwargs: log['kwargs'] = json.dumps(kwargs)
    print(log)
    sys.stdout.flush()
    return True
 
#
 
app_start_time = get_epoch()
 
def get_data():
    p = subprocess.Popen(['/home/genesys/mlcmd_fastapi/mlcmd_getallappstatus.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    data = stdout.decode()
    return json.loads(data)
 
     
@app.get("/")
async def index():
    data = get_data()
    dd(data)
    return data
 
 
@app.get("/info")
async def info():
    data = {
    'hostname': get_hostname(),
    'app-name': get_appname(),
    'app-start-time': app_start_time,
    'app-uptime': get_app_uptime(),
    'pid': get_pid(),
    'now': get_now(),
    'now_utc': get_now_utc(),
    'request-ts': get_epoch(),
    'request-ns': get_epoch_nanoseconds(),
    'version': __version__
    }
    dd(data)
    return data
 
 
if __name__ == "__main__":
 
    dd("Starting [mlcmd_api]")
     
    uvicorn.run("app:app", host="0.0.0.0", port=APP_PORT, reload=True, access_log=True)

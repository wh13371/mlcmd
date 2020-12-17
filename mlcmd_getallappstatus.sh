#! /bin/bash
 
CSHOST=<CHANGEME!!!>
CSPORT=2020
CSAPP=default
CSUID=<CHANGEME!!!>
CSPWD=<CHANGEME!!!>
SCSHOST=<CHANGEME!!!>
SCSPORT=<CHANGEME!!!>
 
mlcmdpath=/home/genesys/gcti/scs_utils
 
_NOW=$(date +"%Y-%m-%dT%H:%M:%S.%6N%Z")
_EPOCH=$(date +"%s.%6N")
_NOW_UTC=$(date --utc +%FT%T.%6N%Z)
 
all_apps_status=$($mlcmdpath/mlcmd_64 \
-cshost $CSHOST -csport $CSPORT -csappname $CSAPP \
-csuser $CSUID -cspassword $CSPWD \
-scshost $SCSHOST -scsport $SCSPORT \
-getallappstatus 2>&1)
 
all_apps=$(printf '%s\n' "$all_apps_status" | awk '\
BEGIN { printf  "{\n\"timestamp\": \"'${_NOW}'\",\n\"epoch\": \"'${_EPOCH}'\",\n\"timestamp_utc\": \"'${_NOW_UTC}'\", \"status_apps_all\":[" } \
/^Application/ { printf  "{\"" $1 "\"" ": \"" $2 "\"," } \
/^DBID/ { printf " \"" $1 "\"" ": \"" $2 "\"," } \
/^Status/ { printf " \"" $1 "\"" ": \"" $2 "\"," } \
/^Runmode/ { printf " \"" $1 "\"" ": \"" $2 "\" },\n" } \
END { printf  "]\n}\n" } \
' \
| sed 's/Application:/Application/g;s/DBID:/DBID/g;s/Status:/Status/g;s/Runmode:/Runmode/g')
 
echo $all_apps | sed 's/\(.*\),/\1 /'

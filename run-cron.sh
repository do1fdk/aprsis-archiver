#!/bin/sh

# Configure this script in your crontab (crontab -e):
# 0 0 * * * /path/to/run-cron.sh

# Path in which the raw data will be stored
DATDIR="/path/to/data"
# Path to aprsis-archiver script
APRSISARCHIVER="/path/to/aprsis-archiver.py"
# Configure your call
MYCALL="N0CALL-PY"

# Choose an APRS-IS server (e.g., nuremberg.aprs2.net:10151 for archiving the
# full feed)
HOST=""
PORT=""

# Path to temporarly store process id (e.g., /var/run)
PIDFILE="/tmp/aprscapture.pid"

if [ ! -x $APRSISARCHIVER ]; then
	echo "ERROR: Path to aprsis-archiver.py not found or not executable: $APRSISARCHIVER"
	exit 1
fi

if [ ! -d $DATDIR ]; then
	echo "ERROR: Data dir $DATDIR doesn't exist"
	exit 1
fi

if [ -s $PIDFILE ]; then
	kill -s 15 $(cat $PIDFILE)
fi

DATE=$(date "+%Y-%m-%d")
$APRSISARCHIVER --file=$DATDIR/aprsis-$DATE.bz2 --host=$HOST --port=$PORT --user=$MYCALL &
echo $! > $PIDFILE

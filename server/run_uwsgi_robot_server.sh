#!/bin/bash
# This script launch the sellit server.
# Usage:
# >./run_uwsgi_sellit_server.sh </path/to/config/file.conf>

# Execute the .conf file.
. $1

# Add some directories to the python path
export PYTHONPATH=$VISIOBOT_HOME/server/:$PYTHONPATH

# Create the log file
touch $VISIOBOT_LOGFILE
touch $VISIOBOT_ACCESS_LOGFILE

# Start the server with uwsgi
echo -n "Start VisioBot server with uWSGI"
exec uwsgi --http-socket :$VISIOBOT_PORT \
           --wsgi-file $VISIOBOT_HOME/server/robot_server.py \
           --callable app \
           --set-placeholder log_file=$VISIOBOT_LOGFILE \
           --logto $VISIOBOT_ACCESS_LOGFILE \
           --logformat "$VISIOBOT_LOG_FORMAT"


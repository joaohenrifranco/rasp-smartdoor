#! /bin/sh

### BEGIN INIT INFO
# Provides:          smart_door.sh
# Required-Start:    $network $syslog
# Required-Stop:     $network $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start smart_door.sh at boot time
# Description:       Enable service provided by smart_door.sh.
### END INIT INFO

nohup python /home/pi/raspdoor/main.py &

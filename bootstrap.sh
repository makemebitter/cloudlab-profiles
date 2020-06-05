#!/bin/bash
set -e

duty=${1}
HOSTS_DIR=/local/host_list
# --------------------- Check if every host online ----------------------------
awk 'NR>1 {print $NF}' /etc/hosts | grep -v 'master' > $HOSTS_DIR
if [ "$duty" = "m" ]; then
    readarray -t hosts < $HOSTS_DIR
    while true; do
        echo "Checking if other hosts online"
        all_done=true
        for host in "${hosts[@]}"; do
            if nc -w 2 -z $host 22 2>/dev/null; then
                echo "$host ✓"
            else
                echo "$host ✗"
                all_done=false
            fi
        done
        

        if [ "$all_done" = true ] ; then
            break
        else
            echo "WAITING"
            sleep 5s
        fi
    done
fi
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# if [ "$duty" = "m" ]; then
#   # Master bootstrap
# fi
# elif [ "$duty" = "s" ]; then
#   # Slave bootstrap
# fi
# -----------------------------------------------------------------------------

echo "Bootstraping complete"










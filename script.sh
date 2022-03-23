while true
    do
        echo "$(date) $(top -p 2169 -b -n 1 | tail -1 | tr -s ' ' | cut -d ' ' -f10,11)" >> log.txt;
        sleep 1;
    done
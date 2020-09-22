#!/bin/sh

echoRed() { echo $'\e[0;31m'"$1"$'\e[0m'; }
echoGreen() { echo $'\e[0;32m'"$1"$'\e[0m'; }
echoYellow() { echo $'\e[0;33m'"$1"$'\e[0m'; }

action=$1

start(){
    echoGreen "starting zkserver..."
    nohup zkServer.sh start > /dev/null 2>&1 &
    sleep 10 
    echoGreen "started zkserver"
    
    
    echoGreen "starting nimbus..."
    nohup storm nimbus >/dev/null 2>&1 &
    sleep 5
    echoGreen "started nimbus"
    
    echoGreen "starting supervisor..."
    nohup storm supervisor >/dev/null 2>&1 &
    sleep 5
    echoGreen "started supervisor"
    
    echoGreen "starting ui..."
    nohup storm ui >/dev/null 2>&1 &
    sleep 5
    echoGreen "started ui"
}

stop() {
    jps | grep -vi jps | awk '{print $1}' | xargs kill -9
}

# storm jar data-clean.jar com.dt.DataCleanTopology  arg1

case "$action" in
start)
    start
    ;;
stop)
    stop
    ;;
*)
    echoYellow "pls input start or stop"
    ;;
esac

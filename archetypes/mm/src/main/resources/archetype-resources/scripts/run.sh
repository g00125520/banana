#!/bin/sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo ${DIR}

action=$1

echoRed() { echo $'\e[0;31m'"$1"$'\e[0m'; }
echoGreen() { echo $'\e[0;32m'"$1"$'\e[0m'; }
echoYellow() { echo $'\e[0;33m'"$1"$'\e[0m'; }

usage() {
	echo $'\n\n\n'
	echoRed "Usage: ${0} support command {start|stop|restart|status|cleanup}"
	echo $'\n\n\n'
	exit 1
}

psCheck() {
	echo "--------------All instances on this machine--------------"
	echo "USER       PID   %CPU %MEM VSZ    RSS    TTY   STAT  START   TIME COMMAND" && echo ""
	ps aux | grep "$APP_NAME" | grep -E -v "grep"
}

[ $# -gt 0 ] || usage

BASE_ARGS="--spring.profiles.active=$PROFILES_ACTIVE --server.port=$SERVER_PORT"

if [ ! "$DISCOVERY_URI" = "" ]; then
	BASE_ARGS="$BASE_ARGS --eureka.client.serviceUrl.defaultZone=$DISCOVERY_URI"
fi

RUN_EXE="$JAVA_EXE $JVM_ARGS -jar $APP_JAR $BASE_ARGS $CMD_LINE_ARGS"

build() {
    mvn clean install
}

isRunning() {
	[[ -f "$PID_FILE" ]] || return 1
	ps -p "$(<"$PID_FILE")" &>/dev/null
}

start() {
    echoGreen "starting ${rootArtifactId}-eureka ..." 
    nohup java -Xms128m -Xmx256m -Xdebug \
         -Xrunjdwp:server=y,transport=dt_socket,address=8881,suspend=n \
         -jar ${rootArtifactId}-eureka/target/${rootArtifactId}-eureka-${version}.jar > ${rootArtifactId}-eureka.log 2>&1 &
    #echo $! velocity can not show !
    sleep 10
    echoGreen "started ${rootArtifactId}-eureka " 
    echoGreen "starting ${rootArtifactId}-config..." 
    nohup java -Xms128m -Xmx256m -Xdebug \
         -Xrunjdwp:server=y,transport=dt_socket,address=8886,suspend=n \
         -jar ${rootArtifactId}-config/target/${rootArtifactId}-config-${version}.jar > ${rootArtifactId}-config.log 2>&1 &
    #echo $! velocity can not show !
    sleep 10
    #echo $! >"$PID_FILE"
    #eureka_pid = `lsof -i:8761 | grep "LISTEN" | awk '{print $2}'`
    #until [ -n "$eureka_pid" ]
    #do 
    #   eureka_pid = `lsof -i:8761 | grep "LISTEN" | awk '{print $2}'`
    #done
    echoGreen "started ${rootArtifactId}-config" 

    echoGreen "starting ${rootArtifactId}-h2 ..." 
    nohup java -Xms128m -Xmx256m -Xdebug \
         -Xrunjdwp:server=y,transport=dt_socket,address=8882,suspend=n \
         -jar ${rootArtifactId}-h2/target/${rootArtifactId}-h2-${version}.jar > ${rootArtifactId}-h2.log 2>&1 &
    #echo $!
    sleep 6
    #h2_pid = `lsof -i:8081 | grep "LISTEN" | awk '{print $2}'`
    #until [ -n "$h2_pid" ]
    #do 
    #   h2_pid = `lsof -i:8081 | grep "LISTEN" | awk '{print $2}'`
    #done
    echoGreen "started ${rootArtifactId}-h2" 

    echoGreen "starting ${rootArtifactId}-consumer ..." 
    nohup java -Xms128m -Xmx256m -Xdebug \
         -Xrunjdwp:server=y,transport=dt_socket,address=8883,suspend=n \
         -jar ${rootArtifactId}-consumer/target/${rootArtifactId}-consumer-${version}.jar > ${rootArtifactId}-consumer.log 2>&1 &
    #echo $!
    sleep 6
    #consumer_pid = `lsof -i:8082 | grep "LISTEN" | awk '{print $2}'`
    #until [ -n "$consumer_pid" ]
    #do 
    #   consumer_pid = `lsof -i:8082 | grep "LISTEN" | awk '{print $2}'`
    #done
    echoGreen "started ${rootArtifactId}-consumer" 
    echoGreen "starting ${rootArtifactId}-hystrix-dashboard..." 
    nohup java -Xms128m -Xmx256m -Xdebug \
         -Xrunjdwp:server=y,transport=dt_socket,address=8884,suspend=n \
         -jar ${rootArtifactId}-hystrix-dashboard/target/${rootArtifactId}-hystrix-dashboard-${version}.jar > ${rootArtifactId}-dashboard.log 2>&1 &
    sleep 6
    echoGreen "started ${rootArtifactId}-hystrix-dashboard" 
    echoGreen "starting ${rootArtifactId}-zuul..." 
    nohup java -Xms128m -Xmx256m -Xdebug \
         -Xrunjdwp:server=y,transport=dt_socket,address=8885,suspend=n \
         -jar ${rootArtifactId}-zuul/target/${rootArtifactId}-zuul-${version}.jar > ${rootArtifactId}-zuul.log 2>&1 &
    sleep 6
    echoGreen "started ${rootArtifactId}-zuul" 
}

stop() {
    jps | grep -vi jps | awk '{print $1}' | xargs kill -9
}

case "$action" in 
build)
    build
    ;;
start)
    start
    ;;
stop)
    stop
    ;;
*)
    usage
    ;;
esac

exit 0


# tell Maven to fork a separate JVM to run your application, rather than it running in the same JVM as Maven
# mvn spring-boot:run -Dfork=true
# cd ${rootArtifactId}-eureka &&  mvn spring-boot:run -Dfork=true
# cd ../${rootArtifactId}-h2 &&  mvn spring-boot:run -Dfork=true
# cd ../${rootArtifactId}-consumer &&  mvn spring-boot:run -Dfork=true
# java -Xms128m -Xmx256m -Xdebug -Xrunjdwp:server=y,transport=dt_socket,address=8081,suspend=n -jar /data/app/test.jar --spring.profiles.active=dev &

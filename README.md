# use spring cloud

use spring cloud

eureka

## micro services

in short, the microservice architectural style is an approach to developing a single application as a suite of small services, each running in its own process and communicating with lightweight mechanisms,offen an http resource api.these services are built around business capabilities and independently deployable by fully automated deployment machinery. there is a bare minimum of centralized management of these services. which may be written in different programming languages and use different data storage technologies.

## ddd

[domain driven design](https://www.infoq.cn/article/domain-driven-design-quickly/) | [12 factor](https://12factor.net/zh_cn/) | [conway law](https://www.infoq.cn/article/every-architect-should-study-conway-law/) | [solid](https://blog.csdn.net/rocketeerli/article/details/81585705)

bounded context

## mq

[rest](http://www.uml.org.cn/zjjs/201805142.asp) | [amqp](https://blog.csdn.net/weixin_37641832/article/details/83270778) | [stomp](https://blog.csdn.net/jhfyuf/article/details/86800382) | [mqtt](https://blog.csdn.net/weixin_43214364/article/details/82719263)

## maven archetypes

mvn archetype:generate -DarchetypeGroupId=org.apache.maven.archetypes -DarchetypeArtifactId=maven-archetype-archetype -DarchetypeVersion=1.4 -DgroupId=com.laodao -DartifactId=mm -Dversion=1.0-SNAPSHOT

mvn archetype:generate -DarchetypeGroupId=com.laodao -DarchetypeCatalog=local -DarchetypeArtifactId=mm -DarchetypeVersion=1.0-SNAPSHOT -DgroupId=com.ld -DartifactId=sc -Dversion=1.0-SNAPSHOT

mvn archetype:generate -DarchetypeGroupId=com.laodao -DarchetypeCatalog=local -DarchetypeArtifactId=storm -DarchetypeVersion=1.0-SNAPSHOT -DgroupId=com.dt -DartifactId=dataclean2 -Dversion=1.0-SNAPSHOT

[mvn archetype:create-from-project](http://maven.apache.org/archetype/maven-archetype-plugin/create-from-project-mojo.html)

archetype:create-from-project -DpackageName=com.laodao，告诉create-from-project命令项目的基础包是什么,防止archetype个别情况猜测包路径错误；

&lt;fileSet filtered="true" packaged="true"> :  filtered表示是否对形如${x}这样的参数进行替换;packaged表示是否将该目录下的内容放入到生成项目的包路径下

\#set( $symbol_pound = '#' )  velocity自定义变量，new Debug("${symbol_pound}${symbol_pound}${symbol_pound}${symbol_pound}${symbol_pound} vehicles")

## jdt

[https://github.com/eclipse/eclipse.jdt.ls](https://github.com/eclipse/eclipse.jdt.ls)

## hystrix

[hystrix wiki](https://github.com/Netflix/Hystrix/wiki/How-To-Use) | [hystrix configuration](https://github.com/Netflix/Hystrix/wiki/Configuration)

## zuul

[use zuul](https://github.com/Netflix/zuul/wiki/How-We-Use-Zuul-At-Netflix)

## rxjava

[rxjava](https://www.jianshu.com/p/cd3557b1a474) | [awesome rx](https://github.com/lzyzsd/Awesome-RxJava)

## dapper

[dapper](https://github.com/bigbully/Dapper-translation) | [zipkin](https://github.com/openzipkin/zipkin/wiki)

## docker

[docker maven plugin](https://github.com/spotify/docker-maven-plugin)

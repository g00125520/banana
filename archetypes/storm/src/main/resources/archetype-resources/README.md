# storm

[storm starter](https://github.com/apache/storm/tree/master/examples/storm-starter) | [document](http://storm.apache.org/releases/2.2.0/)

zkServer.sh start

./storm nimbus >/dev/null 2>&1 &

./storm supervisor >/dev/null 2>&1 &

./storm ui >/dev/null 2>&1 &

bin/storm jar data-clean.jar com.dt.DataCleanTopology  arg1

sed -i "s/org\.apache\.storm\.starter/\$\{package\}/g"  `grep -rl 'org\.apache\.storm\.starter' .`

## grouping

fieldsGrouping: 按照某个字段进行分组，具有同样字段值的tuple会被分配到相同的bolts，而不同的字段值的tuple则被分配到不同的bolts；

shuffleGrouping: 随机分组，随机派发stream里面的tuple，保证每个bolt接收到的tuple数目相同。轮询，平均分配；

globalGrouping: 全局分组，这个tuple会被分配到storm的一个bolt的其中一个task，也就是id值最低的那个task；

allGrouping: 广播发送，对于每一个tuple所有的bolts都收到；

nonGrouping: 不分组，stream不关心那个bolt会收到它的tuple；

directGrouping: 消息的发送者决定由消息接收者的那个task处理消息，

## common patterns in storm

[common patterns](http://storm.apache.org/releases/2.2.0/Common-patterns.html)

## distributed rpc 

[distributed rpc](http://storm.apache.org/releases/current/Distributed-RPC.html)

## ack机制

acker跟踪算法对于任意大的一个tuple树，只需恒定的20字节就可以进行跟踪，其原理为：acker对每个spout-tuple保存一个ack-val的校验值，它的初始值为0，然后每发射一个tuple或ack一个tuple时，这个tuple的id就跟这个校验值异或一下，并且把得到的值更新为ack-val的新值，那么假设每个发射出去的tuple都被ack了，那么最后ack-val的值就一定是0。acker就根据ack-val的值是否为0来判断是否完全处理。

实现ack机制：1，spout发射tuple时指定msgid；2，spout重写baserichspout的ack和fail方法；3，spout对发射的tuple进行缓存，否则spout的fail方法收到acker的msgid，无法获取失败的数据重新发送；4，spout根据msgid对ack的tuple从缓存队列中删除，对fail的tuple选择重新发送；5，设置acker数至少大于0：Config.setNumAckers(conf, ackerParal);

bolt分basicbolt和richbolt。在basicbolt中，basicoutputcollector在emit时会自动和输入的tuple相关联，而在execute方法结束的时候，输入的tuple会被自动ack；在richbolt中，需要在emit数据时，需显式指定该数据的源tuple，以保持tracker链路，collector.emit(oldTuple, newTuple);并execute成功后调用OutputCollector.ack(tuple),失败时调用OutputCollector.fail(tuple);如在richbolt中忘了标识锚点，就是忘了标识血缘关系，storm会认为你不关心后面阶段的处理状况；忘了手动ack或fail，storm框架会等待反馈，达到超时阈值之后，就直接给fail。

关闭ack机制：1，spout发送数据时不带msgid；2，设置acker数等于0，Config.TOPOLOGY_ACKERS；3，如果不在意某个消息派生出来的子孙消息的可靠性，则发送子孙消息的时候不做锚定，即再emit方法中不指定输入消息，因为子孙消息没有被锚定在任何tuple tree中，因此它们的失败不引起任何spout的重发。由一个tuple产生一个新的tuple称为：anchoring，你发射一个tuple的同时也就完成了一次anchoring。

ack还常用于限流，为避免spout发送数据过快，而bolt处理太慢，常设置pending数：conf.put(Config.TOPOLOGY_MAX_SPOUT_PENDING, pending)；当spout有等于或超过pengding数的tuple没有收到ack或fail响应时，跳过执行nexttuple，从而限制spout发送数据。

## trident

[trident tutorial](http://storm.apache.org/releases/current/Trident-tutorial.html) | [trident state](http://storm.apache.org/releases/current/Trident-state.html) | [trident](http://www.tianshouzhi.com/api/tutorials/storm/57)

1，每个批处理都会生成一个事务id，如果一个批处理重复执行，则事务id是重复的；2，批处理的状态更新是按照顺序执行的，批处理3的状态更新只有在2更新成功之后才会执行；

## 定时机制，tickTuple

tick机制可让任何bolt每隔一段时间，通过conf.put(Config.TOPOLOGY_TICK_TUPLE_FREQ_SECS, 间隔时间)设置，收到一个tickTuple，bolt收到后可根据业务需求完成处理，从而实现定时处理功能。tickTuple可根据TupleUtils.isTick方法进行判断。

## window

[windowing](http://storm.apache.org/releases/2.2.0/Windowing.html)

watermark，最大tuple的时间戳-lag为watermark，因为，早于该时间点的tuple不应该再纳入window处理了，如果之后才到来，则被认为是迟到的tuple而被丢弃；最新的window边界到watermark，超出的tuple纳入下次计算的window中处理；

tumbling window只有get方法，返回window内的所有tuple，而sliding window还有getnew和getexpired方法，sliding window规定了window的大小和滑动的间隔，getnew返回刚滑动进来的tuple，getexpired返回刚滑动出去的tuple；

# flux

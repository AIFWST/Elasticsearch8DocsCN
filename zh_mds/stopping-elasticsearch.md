

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md)

[« Starting Elasticsearch](starting-elasticsearch.md) [Discovery and cluster
formation »](modules-discovery.md)

## 停止弹性搜索

有序关闭 Elasticsearch 可确保 Elasticsearch 有机会清理和关闭未完成的资源。例如，以有序方式关闭的节点将从群集中删除自身，将事务日志同步到磁盘，并执行其他相关的清理活动。您可以通过正确停止 Elasticsearch 来帮助确保有序关机。

如果您将 Elasticsearch 作为服务运行，则可以通过安装提供的服务管理功能来停止 Elasticsearch。

如果您直接运行 Elasticsearch，则可以通过发送 control-C 来停止 Elasticsearch(如果您在控制台中运行 Elasticsearch)，或者通过将"SIGTERM"发送到 POSIX 系统上的 Elasticsearch 进程。您可以通过各种工具(例如，"ps"或"jps")获取 PID 以发送信号：

    
    
    $ jps | grep Elasticsearch
    14542 Elasticsearch

从 Elasticsearch 启动日志：

    
    
    [2016-07-07 12:26:18,908][INFO ][node                     ] [I8hydUG] version[5.0.0-alpha4], pid[15399], build[3f5b994/2016-06-27T16:23:46.861Z], OS[Mac OS X/10.11.5/x86_64], JVM[Oracle Corporation/Java HotSpot(TM) 64-Bit Server VM/1.8.0_92/25.92-b14]

或者通过指定启动时写入 PID 文件的位置 ('-p <path>')：

    
    
    $ ./bin/elasticsearch -p /tmp/elasticsearch-pid -d
    $ cat /tmp/elasticsearch-pid && echo
    15516
    $ kill -SIGTERM 15516

### 在致命错误时停止

在 Elasticsearch 虚拟机的生命周期内，可能会出现某些致命错误，使虚拟机处于可疑状态。此类致命错误包括内存不足错误、虚拟机中的内部错误以及严重的 I/O 错误。

当 Elasticsearch 检测到虚拟机遇到此类致命错误时，Elasticsearch 将尝试记录该错误，然后停止虚拟机。当 Elasticsearch 启动此类关机时，它不会经历如上所述的有序关机。Elasticsearch 进程还将返回一个特殊的状态代码，指示错误的性质。

JVM 内部错误

|

128 ---|--- 内存不足错误

|

127 堆栈溢出错误

|

126 未知虚拟机错误

|

125 严重 I/O 错误

|

124 未知致命错误

|

1 « 启动 Elasticsearch 发现和集群形成 »
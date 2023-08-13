

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up a
cluster for high availability](high-availability.md) ›[Cross-cluster
replication](xpack-ccr.md)

[« Tutorial: Disaster recovery based on uni-directional cross-cluster
replication](ccr-disaster-recovery-uni-directional-tutorial.md) [Snapshot
and restore »](snapshot-restore.md)

## 教程：基于双向跨集群复制的容灾

了解如何基于双向跨集群复制在两个集群之间设置灾难恢复。以下教程专为支持按查询更新和按查询删除的数据流而设计。您只能对领导者索引执行这些操作。

本教程使用 Logstash 作为摄取源。它利用了 Logstash 功能，其中 Logstash 输出到Elasticsearch可以在指定的主机阵列之间进行负载平衡。Beats 和弹性代理目前不支持多个输出。在本教程中，还应该可以设置一个代理(负载均衡器)来重定向流量，而无需 Logstash。

* 在"集群 A"和"集群 B"上设置远程集群。  * 使用排除模式设置双向跨集群复制。  * 设置具有多个主机的 Logstash，以便在灾难发生时自动进行负载平衡和切换。

!双向跨群集复制故障转移和故障回复

### 初始化设置

1. 在两个集群上设置远程集群。           响应 = client.cluster.put_settings( 正文： { 持久： { 集群： { 远程： { "集群B"： { 模式： '代理'， skip_unavailable： 真， server_name： 'clusterb.es.region-b.gcp.elastic-cloud.com'， proxy_socket_connections： 18， proxy_address： 'clusterb.es.region-b.gcp.elastic-cloud.com:9400' } } } ) 放置响应       响应 = client.cluster.put_settings( 正文： { 持久： { 集群： { 远程： { "集群A"： { 模式： '代理'， skip_unavailable： true， server_name： 'clustera.es.region-a.gcp.elastic-cloud.com'， proxy_socket_connections： 18， proxy_address： 'clustera.es.region-a.gcp.elastic-cloud.com:9400' } } } ) 放置响应           ### 在集群 A 上 ### PUT _cluster/设置 { "持久"： { "集群"： { "远程"： { "集群B"： { "模式"： "代理"， "skip_unavailable"： true， "server_name"： "clusterb.es.region-b.gcp.elastic-cloud.com"， "proxy_socket_connections"： 18， "proxy_address"： "clusterb.es.region-b.gcp.elastic-cloud.com:9400" } } } ### 在集群 B 上 ### PUT _cluster/设置   { "持久"： { "集群"： { "远程"： { "clusterA"： { "mode"： "proxy"， "skip_unavailable"： true， "server_name"： "clustera.es.region-a.gcp.elastic-cloud.com"， "proxy_socket_connections"： 18， "proxy_address"： "clustera.es.region-a.gcp.elastic-cloud.com:9400" } } } } }

2. 设置双向跨集群复制。           ### 在集群 A 上 ### PUT /_ccr/auto_follow/logs-generic-default { "remote_cluster"： "clusterB"， "leader_index_patterns"： [ ".ds-logs-generic-default-20*" ]， "leader_index_exclusion_patterns"："{{leader_index}}-replicated_from_clustera"， "follow_index_pattern"： "{{leader_index}}-replicated_from_clusterb" } ### 在集群 B 上 ### PUT /_ccr/auto_follow/logs-generic-default { "remote_cluster"： "clusterA"， "leader_index_patterns"： [       ".ds-logs-generic-default-20*" ]， "leader_index_exclusion_patterns"："{{leader_index}}-replicated_from_clusterb"， "follow_index_pattern"： "{{leader_index}}-replicated_from_clustera" }

群集上的现有数据不会通过"_ccr/auto_follow"复制，即使模式可能匹配。此函数将仅复制新创建的后备索引(作为数据流的一部分)。

使用"leader_index_exclusion_patterns"以避免递归。

"follow_index_pattern"仅允许小写字符。

由于 UI 中缺少排除模式，因此无法通过 Kibana UI 执行此步骤。在此步骤中使用 API。

3. 设置 Logstash 配置文件。

此示例使用输入生成器来演示群集中的文档计数。重新配置此部分以适合您自己的用例。

    
        ### On Logstash server ###
    ### This is a logstash config file ###
    input {
      generator{
        message => 'Hello World'
        count => 100
      }
    }
    output {
      elasticsearch {
        hosts => ["https://clustera.es.region-a.gcp.elastic-cloud.com:9243","https://clusterb.es.region-b.gcp.elastic-cloud.com:9243"]
        user => "logstash-user"
        password => "same_password_for_both_clusters"
      }
    }

关键点是，当"集群 A"关闭时，所有流量将自动重定向到"集群 B"。一旦"集群 A"返回，流量就会再次自动重定向回"集群 A"。这是通过选项"主机"实现的，其中在阵列"[集群 A， 集群 B]"中指定了多个 ES 集群端点。

为两个群集上的同一用户设置相同的密码以使用此负载平衡功能。

4. 使用较早的配置文件启动 Logstash。           ### 在 Logstash 服务器上 ### bin/logstash -f multiple_hosts.conf

5. 观察数据流中的文档计数。

安装程序在每个群集上创建一个名为"logs-generic-default"的数据流。当两个集群都启动时，Logstash 会将 50% 的文档写入"集群 A"，将 50% 的文档写入"集群 B"。

双向跨集群复制将在后缀为"-replication_from_cluster{a|b}"的每个集群上再创建一个数据流。在此步骤结束时：

    * data streams on cluster A contain:

      * 50 documents in `logs-generic-default-replicated_from_clusterb`
      * 50 documents in `logs-generic-default`

    * data streams on cluster B contain:

      * 50 documents in `logs-generic-default-replicated_from_clustera`
      * 50 documents in `logs-generic-default`

6. 应将查询设置为跨两个数据流进行搜索。对任一集群上的"logs*"进行查询总共返回 100 次命中。           响应 = client.search( index： 'logs*'， size： 0 ) put response get logs*/_search？size=0

### "clusterA"关闭时的故障转移

1. 您可以通过关闭任一集群来模拟这种情况。让我们在本教程中关闭"集群 A"。  2. 使用相同的配置文件启动 Logstash。(在 Logstash 连续摄取的实际用例中，此步骤不是必需的。           ### 在 Logstash 服务器上 ### bin/logstash -f multiple_hosts.conf

3. 观察所有 Logstash 流量将自动重定向到"集群 B"。

在此期间，还应将所有搜索流量重定向到"clusterB"集群。

4. "提案集 B"上的两个数据流现在包含不同数量的文档。

    * data streams on cluster A (down)

      * 50 documents in `logs-generic-default-replicated_from_clusterb`
      * 50 documents in `logs-generic-default`

    * data streams On cluster B (up)

      * 50 documents in `logs-generic-default-replicated_from_clustera`
      * 150 documents in `logs-generic-default`

### "clusterA"返回时故障回复

1. 您可以通过重新打开"集群 A"来模拟这种情况。  2. 在"集群 A"停机期间摄取到"集群 B"的数据将自动复制。

    * data streams on cluster A

      * 150 documents in `logs-generic-default-replicated_from_clusterb`
      * 50 documents in `logs-generic-default`

    * data streams on cluster B

      * 50 documents in `logs-generic-default-replicated_from_clustera`
      * 150 documents in `logs-generic-default`

3. 如果此时正在运行 Logstash，您还将观察到流量被发送到两个集群。

### 按查询执行更新或删除

可以更新或删除文档，但只能对领导者索引执行这些操作。

1. 首先确定哪个后备索引包含要更新的文档。           response = client.search( index： 'logs-generic-default*'， filter_path： 'hits.hits._index'， body： { query： { match： { "event.sequence"： '97' } } } ) 将响应 ### 放在任一集群上 ### GET logs-generic-default*/_search？filter_path=hits.hits._index { "query"： { "match"： { "event.sequence"： "97" } } }

    * If the hits returns `"_index": ".ds-logs-generic-default-replicated_from_clustera-<yyyy.MM.dd>-*"`, then you need to proceed to the next step on `cluster A`. 
    * If the hits returns `"_index": ".ds-logs-generic-default-replicated_from_clusterb-<yyyy.MM.dd>-*"`, then you need to proceed to the next step on `cluster B`. 
    * If the hits returns `"_index": ".ds-logs-generic-default-<yyyy.MM.dd>-*"`, then you need to proceed to the next step on the same cluster where you performed the search query. 

2. 通过查询执行更新(或删除)：响应 = client.update_by_query( 索引："日志通用默认值"，正文：{ 查询：{ 匹配：{ "事件序列"：'97' } }，脚本：{ 源："ctx._source.event.original = params.new_event"，语言："无痛"，参数：{ new_event："FOOBAR" } } } } ) 将响应 ### 放在从上一个标识的集群上步骤 ### POST 日志-通用默认/_update_by_query { "query"： { "match"： { "event.sequence"： "97" } }， "script"： { "source"： "ctx._source.event.original = params.new_event"， "lang"： "painless"， "params"： { "new_event"： "FOOBAR" } } }

如果软删除在复制到追随者之前被合并，则由于领导者的历史记录不完整，以下过程将失败，seeindex.soft_deletes.retention_lease.period了解更多详细信息。

[« Tutorial: Disaster recovery based on uni-directional cross-cluster
replication](ccr-disaster-recovery-uni-directional-tutorial.md) [Snapshot
and restore »](snapshot-restore.md)

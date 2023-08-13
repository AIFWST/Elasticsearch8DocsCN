

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up a
cluster for high availability](high-availability.md) ›[Cross-cluster
replication](xpack-ccr.md)

[« Upgrading clusters using cross-cluster replication](ccr-upgrading.md)
[Tutorial: Disaster recovery based on bi-directional cross-cluster replication
»](ccr-disaster-recovery-bi-directional-tutorial.md)

## 教程：基于单向跨集群复制的容灾

了解如何基于单向跨集群复制在两个集群之间进行故障转移和故障回复。您还可以访问双向灾难恢复以设置复制数据流，这些数据流无需人工干预即可自动故障转移和故障回复。

* 设置从"集群 A"复制到"集群 B"的单向跨集群复制。  * 故障转移 - 如果"clusterA"脱机，"clusterB"需要将追随者索引"提升"为常规索引以允许写入操作。所有摄取都需要重定向到"clusterB"，这由客户端(Logstash、Beats、Elastic Agents 等)控制。  * 故障回复 - 当"clusterA"重新联机时，它承担追随者的角色，并从"clusterB"复制领导者索引。

!单向跨群集复制故障转移和故障回复

跨集群复制提供仅复制用户生成的索引的功能。跨群集复制不是为复制系统生成的索引或快照设置而设计的，并且无法跨群集复制 ILM 或 SLM 策略。有关详细信息，请参阅跨集群复制限制。

###Prerequisites

在完成本教程之前，请设置跨集群复制以连接两个集群并配置从属索引。

在本教程中，"kibana_sample_data_ecommerce"从"集群 A"复制到"集群 B"。

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          cluster: {
            remote: {
              "clusterA": {
                mode: 'proxy',
                skip_unavailable: 'true',
                server_name: 'clustera.es.region-a.gcp.elastic-cloud.com',
                proxy_socket_connections: '18',
                proxy_address: 'clustera.es.region-a.gcp.elastic-cloud.com:9400'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    ### On clusterB ###
    PUT _cluster/settings
    {
      "persistent": {
        "cluster": {
          "remote": {
            "clusterA": {
              "mode": "proxy",
              "skip_unavailable": "true",
              "server_name": "clustera.es.region-a.gcp.elastic-cloud.com",
              "proxy_socket_connections": "18",
              "proxy_address": "clustera.es.region-a.gcp.elastic-cloud.com:9400"
            }
          }
        }
      }
    }
    
    
    ### On clusterB ###
    PUT /kibana_sample_data_ecommerce2/_ccr/follow?wait_for_active_shards=1
    {
      "remote_cluster": "clusterA",
      "leader_index": "kibana_sample_data_ecommerce"
    }

写入(如引入或更新)应仅在领导者索引上进行。追随者索引是只读的，将拒绝任何写入。

### "clusterA"关闭时的故障转移

1. 将"clusterB"中的追随者索引提升为常规索引，以便它们接受写入。这可以通过以下方式实现：

    * First, pause indexing following for the follower index. 
    * Next, close the follower index. 
    * Unfollow the leader index. 
    * Finally, open the follower index (which at this point is a regular index). 
    
        response = client.ccr.pause_follow(
      index: 'kibana_sample_data_ecommerce2'
    )
    puts response
    
    response = client.indices.close(
      index: 'kibana_sample_data_ecommerce2'
    )
    puts response
    
    response = client.ccr.unfollow(
      index: 'kibana_sample_data_ecommerce2'
    )
    puts response
    
    response = client.indices.open(
      index: 'kibana_sample_data_ecommerce2'
    )
    puts response
    
        ### On clusterB ###
    POST /kibana_sample_data_ecommerce2/_ccr/pause_follow
    POST /kibana_sample_data_ecommerce2/_close
    POST /kibana_sample_data_ecommerce2/_ccr/unfollow
    POST /kibana_sample_data_ecommerce2/_open

2. 在客户端(Logstash、Beats、Elastic Agent)，手动重新启用"kibana_sample_data_ecommerce2"摄取并将流量重定向到"clusterB"。在此期间，还应将所有搜索流量重定向到"clusterB"群集。可以通过将文档引入此索引来模拟这种情况。您应该注意到此索引现在是可写的。           ### On clusterB ### POST kibana_sample_data_ecommerce2/_doc/ { "user"： "kimchy" }

### "clusterA"返回时故障回复

当"集群A"回来时，"集群B"成为新的领导者，"集群A"成为追随者。

1. 在"集群 A"上设置远程集群"集群 B"。           响应 = client.cluster.put_settings( 正文： { 持久： { 集群： { 远程： { "集群B"： { 模式： '代理'， skip_unavailable： 'true'， server_name： 'clusterb.es.region-b.gcp.elastic-cloud.com'， proxy_socket_connections： '18'， proxy_address： 'clusterb.es.region-b.gcp.elastic-cloud.com:9400' } } } ) 放置响应           ### 在集群 A 上 ### PUT _cluster/设置 { "持久"： { "集群"： { "远程"： { "clusterB"： { "mode"： "proxy"， "skip_unavailable"： "true"， "server_name"： "clusterb.es.region-b.gcp.elastic-cloud.com"， "proxy_socket_connections"： "18"， "proxy_address"： "clusterb.es.region-b.gcp.elastic-cloud.com:9400" } } }

2. 需要丢弃现有数据，然后才能将任何索引转换为关注者。在删除"clusterA"上的任何索引之前，请确保"clusterB"上的最新数据可用。           响应 = client.index.delete( index： 'kibana_sample_data_ecommerce' ) 将响应 ### 放在集群上 ### 删除kibana_sample_data_ecommerce

3. 在"集群 A"上创建一个追随者索引，现在在"集群 B"中创建领导者索引。           ### On clusterA ### PUT /kibana_sample_data_ecommerce/_ccr/follow？wait_for_active_shards=1 { "remote_cluster"： "clusterB"， "leader_index"： "kibana_sample_data_ecommerce2" }

4. 关注者集群上的索引现在包含更新的文档。           response = client.search( index： 'kibana_sample_data_ecommerce'， q： 'kimchy' ) 将响应 ### 放在集群上 ### GET kibana_sample_data_ecommerce/_search？q=kimchy

如果软删除在复制到追随者之前被合并，则由于领导者的历史记录不完整，以下过程将失败，seeindex.soft_deletes.retention_lease.period了解更多详细信息。

[« Upgrading clusters using cross-cluster replication](ccr-upgrading.md)
[Tutorial: Disaster recovery based on bi-directional cross-cluster replication
»](ccr-disaster-recovery-bi-directional-tutorial.md)

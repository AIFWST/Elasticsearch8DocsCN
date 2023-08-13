

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« License settings](license-settings.md) [Logging »](logging.md)

## 本地网关设置

本地网关在完全集群重启后存储集群状态和分片数据。

必须在每个主节点上设置以下 _static_ 设置，控制新选择的主节点在尝试恢复集群状态和集群数据之前应等待多长时间。

这些设置仅在群集完全重新启动时生效。

`gateway.expected_data_nodes`

     ([Static](settings.html#static-cluster-setting)) Number of data nodes expected in the cluster. Recovery of local shards begins when the expected number of data nodes join the cluster. Defaults to `0`. 
`gateway.recover_after_time`

    

(静态)如果未达到预期的节点数，则恢复过程将等待配置的时间量，然后再尝试恢复。默认为"5m"。

一旦"recover_after_time"持续时间超时，只要满足以下条件，恢复就会开始：

`gateway.recover_after_data_nodes`

     ([Static](settings.html#static-cluster-setting)) Recover as long as this many data nodes have joined the cluster. 

这些设置可以在"elasticsearch.yml"中配置，如下所示：

    
    
    gateway.expected_data_nodes: 3
    gateway.recover_after_time: 600s
    gateway.recover_after_data_nodes: 3

### 悬空指数

当节点加入集群时，如果它发现存储在其本地数据目录中的任何分片在集群中尚不存在，它将认为这些分片属于"悬空"索引。您可以使用悬空索引 API 列出、导入或删除垂钓索引。

当索引仍然是群集的一部分时，API 无法保证导入的数据是否真实地表示数据的最新状态。

[« License settings](license-settings.md) [Logging »](logging.md)

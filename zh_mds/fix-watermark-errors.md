

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md) ›[Fix common cluster issues](fix-
common-cluster-issues.md)

[« Fix common cluster issues](fix-common-cluster-issues.md) [Circuit breaker
errors »](circuit-breaker-errors.md)

## 修复水印错误

当数据节点磁盘空间严重不足且已达到泛洪阶段磁盘使用水位线时，将记录以下错误："错误：磁盘使用率超出泛洪阶段水位线，索引具有只读允许删除块"。

为了防止磁盘已满，当节点达到此水位线时，Elasticsearchblocks 会写入节点上带有分片的任何索引。如果区块影响相关的系统索引，Kibana 和其他 Elastic Stack 功能可能会变得不可用。

当受影响节点的磁盘使用率低于高磁盘水位线时，Elasticsearch 会自动删除写入块。为了实现这一点，Elasticsearch 会自动将一些受影响节点的分片移动到同一数据层中的其他节点。

要验证分片是否正在从受影响的节点移出，请使用 cat 分片 API。

    
    
    response = client.cat.shards(
      v: true
    )
    puts response
    
    
    GET _cat/shards?v=true

如果分片仍保留在节点上，请使用集群分配说明 API 获取其分配状态的说明。

    
    
    response = client.cluster.allocation_explain(
      body: {
        index: 'my-index',
        shard: 0,
        primary: false,
        current_node: 'my-node'
      }
    )
    puts response
    
    
    GET _cluster/allocation/explain
    {
      "index": "my-index",
      "shard": 0,
      "primary": false,
      "current_node": "my-node"
    }

要立即恢复写入操作，您可以暂时增加磁盘水印并删除写入块。

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "cluster.routing.allocation.disk.watermark.low": '90%',
          "cluster.routing.allocation.disk.watermark.low.max_headroom": '100GB',
          "cluster.routing.allocation.disk.watermark.high": '95%',
          "cluster.routing.allocation.disk.watermark.high.max_headroom": '20GB',
          "cluster.routing.allocation.disk.watermark.flood_stage": '97%',
          "cluster.routing.allocation.disk.watermark.flood_stage.max_headroom": '5GB',
          "cluster.routing.allocation.disk.watermark.flood_stage.frozen": '97%',
          "cluster.routing.allocation.disk.watermark.flood_stage.frozen.max_headroom": '5GB'
        }
      }
    )
    puts response
    
    response = client.indices.put_settings(
      index: '*',
      expand_wildcards: 'all',
      body: {
        "index.blocks.read_only_allow_delete": nil
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
      "persistent": {
        "cluster.routing.allocation.disk.watermark.low": "90%",
        "cluster.routing.allocation.disk.watermark.low.max_headroom": "100GB",
        "cluster.routing.allocation.disk.watermark.high": "95%",
        "cluster.routing.allocation.disk.watermark.high.max_headroom": "20GB",
        "cluster.routing.allocation.disk.watermark.flood_stage": "97%",
        "cluster.routing.allocation.disk.watermark.flood_stage.max_headroom": "5GB",
        "cluster.routing.allocation.disk.watermark.flood_stage.frozen": "97%",
        "cluster.routing.allocation.disk.watermark.flood_stage.frozen.max_headroom": "5GB"
      }
    }
    
    PUT */_settings?expand_wildcards=all
    {
      "index.blocks.read_only_allow_delete": null
    }

作为长期解决方案，建议将节点添加到受影响的数据层或升级现有节点以增加磁盘空间。要释放额外的磁盘空间，您可以使用删除索引 API 删除不需要的索引。

    
    
    response = client.indices.delete(
      index: 'my-index'
    )
    puts response
    
    
    DELETE my-index

当长期解决方案到位时，重置或重新配置磁盘水印。

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "cluster.routing.allocation.disk.watermark.low": nil,
          "cluster.routing.allocation.disk.watermark.low.max_headroom": nil,
          "cluster.routing.allocation.disk.watermark.high": nil,
          "cluster.routing.allocation.disk.watermark.high.max_headroom": nil,
          "cluster.routing.allocation.disk.watermark.flood_stage": nil,
          "cluster.routing.allocation.disk.watermark.flood_stage.max_headroom": nil,
          "cluster.routing.allocation.disk.watermark.flood_stage.frozen": nil,
          "cluster.routing.allocation.disk.watermark.flood_stage.frozen.max_headroom": nil
        }
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
      "persistent": {
        "cluster.routing.allocation.disk.watermark.low": null,
        "cluster.routing.allocation.disk.watermark.low.max_headroom": null,
        "cluster.routing.allocation.disk.watermark.high": null,
        "cluster.routing.allocation.disk.watermark.high.max_headroom": null,
        "cluster.routing.allocation.disk.watermark.flood_stage": null,
        "cluster.routing.allocation.disk.watermark.flood_stage.max_headroom": null,
        "cluster.routing.allocation.disk.watermark.flood_stage.frozen": null,
        "cluster.routing.allocation.disk.watermark.flood_stage.frozen.max_headroom": null
      }
    }

[« Fix common cluster issues](fix-common-cluster-issues.md) [Circuit breaker
errors »](circuit-breaker-errors.md)



[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Index
modules](index-modules.md) ›[Index Shard Allocation](index-modules-
allocation.md)

[« Index Shard Allocation](index-modules-allocation.md) [Delaying allocation
when a node leaves »](delayed-allocation.md)

## 索引级分片分配过滤

您可以使用分片分配过滤器来控制 Elasticsearch 分配特定索引的分片的位置。这些按索引筛选器与群集范围的分配筛选和分配感知一起应用。

分片分配过滤器可以基于自定义节点属性或内置的"_name"、"_host_ip"、"_publish_ip"、"_ip"、"_host"、"_id"、"_tier"和"_tier_preference"属性。索引生命周期管理使用基于自定义节点属性的筛选器来确定在阶段之间移动时如何重新分配分片。

"cluster.routeting.allocation"设置是动态的，使现有索引能够立即从一组节点移动到另一组节点。只有在可能的情况下重新定位分片而不会破坏其他路由约束，例如从不在同一节点上分配主分片和副本分片。

例如，您可以使用自定义节点属性来指示节点的性能特征，并使用分片分配筛选将特定索引的分片路由到最合适的硬件类。

#### 启用索引级分片分配筛选

要根据自定义节点属性进行筛选，请执行以下操作：

1. 在每个节点的"elasticsearch.yml"配置文件中使用自定义节点属性指定过滤器特征。例如，如果您有"小"、"中"和"大"节点，则可以添加"size"属性以根据节点大小进行筛选。           节点大小：中等

您还可以在启动节点时设置自定义属性：

    
        ./bin/elasticsearch -Enode.attr.size=medium

2. 向索引添加路由分配筛选器。"index.routing.allocation"设置支持三种类型的过滤器："包含"、"排除"和"要求"。例如，要告诉 Elasticsearch 将分片从"test"索引分配给"大"或"中等"节点，请使用"index.routeting.allocation.include"： response = client.indices.put_settings( index： 'test'， body： { "index.routing.allocation.include.size"： 'big，medium' } ) put response PUT test/_settings { "index.routing.allocation.include.size"： "big，medium" }

如果指定多个筛选器，则节点必须同时满足以下条件，才能将分片重新定位到该节点：

    * If any `require` type conditions are specified, all of them must be satisfied 
    * If any `exclude` type conditions are specified, none of them may be satisfied 
    * If any `include` type conditions are specified, at least one of them must be satisfied 

例如，要将"test"索引移动到"rack1"中的"大"节点，您可以指定：

    
        response = client.indices.put_settings(
      index: 'test',
      body: {
        "index.routing.allocation.require.size": 'big',
        "index.routing.allocation.require.rack": 'rack1'
      }
    )
    puts response
    
        PUT test/_settings
    {
      "index.routing.allocation.require.size": "big",
      "index.routing.allocation.require.rack": "rack1"
    }

#### 索引分配筛选器设置

`index.routing.allocation.include.{attribute}`

     Assign the index to a node whose `{attribute}` has at least one of the comma-separated values. 
`index.routing.allocation.require.{attribute}`

     Assign the index to a node whose `{attribute}` has _all_ of the comma-separated values. 
`index.routing.allocation.exclude.{attribute}`

     Assign the index to a node whose `{attribute}` has _none_ of the comma-separated values. 

索引分配设置支持以下内置属性：

`_name`

|

按节点名称匹配节点 ---|--- '_host_ip'

|

按主机 IP 地址(与主机名关联的 IP)"_publish_ip"匹配节点

|

通过发布 IP 地址"_ip"匹配节点

|

匹配"_host_ip"或"_publish_ip""_host"

|

按主机名"_id"匹配节点

|

按节点 ID "_tier"匹配节点

|

按节点的数据层角色匹配节点。有关详细信息，请参阅数据层分配筛选"_tier"筛选基于节点角色。只有一部分角色是数据层角色，通用数据角色将与任何层筛选匹配。

指定属性值时可以使用通配符，例如：

    
    
    response = client.indices.put_settings(
      index: 'test',
      body: {
        "index.routing.allocation.include._ip": '192.168.2.*'
      }
    )
    puts response
    
    
    PUT test/_settings
    {
      "index.routing.allocation.include._ip": "192.168.2.*"
    }

[« Index Shard Allocation](index-modules-allocation.md) [Delaying allocation
when a node leaves »](delayed-allocation.md)

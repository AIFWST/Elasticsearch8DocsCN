

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Index template exists API](indices-template-exists-v1.md) [Open index API
»](indices-open-close.md)

## 列出悬空索引API

列出悬空索引。

###Request

    
    
    response = client.dangling_indices.list_dangling_indices
    puts response
    
    
    GET /_dangling

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。

###Description

如果 Elasticsearch 遇到当前集群状态中缺少的索引数据，则认为这些索引处于悬空状态。例如，如果您在 Elasticsearch 节点处于脱机状态时删除了多个 'cluster.indices.tombstones.size' 索引，则可能会发生这种情况。

使用此 API 列出悬空索引，然后可以导入或删除这些索引。

###Examples

API 返回以下响应：

    
    
    {
      "dangling_indices": [
       {
        "index_name": "my-index-000001",
        "index_uuid": "zmM4e0JtBkeUjiHD-MihPQ",
        "creation_date_millis": 1589414451372,
        "node_ids": [
          "pL47UN3dAb2d5RCWP6lQ3e"
        ]
       }
      ]
    }

[« Index template exists API](indices-template-exists-v1.md) [Open index API
»](indices-open-close.md)

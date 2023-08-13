

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cluster APIs](cluster.md)

[« Get desired nodes API](get-desired-nodes.md) [Get desired balance API
»](get-desired-balance.md)

## 删除所需节点接口

此功能专为 ElasticsearchService、Elastic Cloud Enterprise 和 Kubernetes 上的 ElasticCloud 间接使用而设计。不支持直接使用。

删除所需的节点。

###Request

    
    
    DELETE /_internal/desired_nodes

###Description

此 API 删除所需的节点。

###Examples

此示例删除当前所需的节点。

    
    
    DELETE /_internal/desired_nodes

[« Get desired nodes API](get-desired-nodes.md) [Get desired balance API
»](get-desired-balance.md)

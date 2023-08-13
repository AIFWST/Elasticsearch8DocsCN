

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cluster APIs](cluster.md)

[« Create or update desired nodes API](update-desired-nodes.md) [Delete
desired nodes API »](delete-desired-nodes.md)

## 获取所需节点API

此功能专为 ElasticsearchService、Elastic Cloud Enterprise 和 Kubernetes 上的 ElasticCloud 间接使用而设计。不支持直接使用。

获取所需的节点。

###Request

    
    
    GET /_internal/desired_nodes/_latest

###Description

此 API 获取所需的最新节点。

###Examples

此示例获取所需的最新节点。

    
    
    GET /_internal/desired_nodes/_latest

API 返回以下结果：

    
    
    {
        "history_id": <history_id>,
        "version": <version>,
        "nodes": [
            {
                "settings": <node_settings>,
                "processors": <node_processors>,
                "memory": "<node_memory>",
                "storage": "<node_storage>",
                "node_version": "<node_version>"
            }
        ]
    }

[« Create or update desired nodes API](update-desired-nodes.md) [Delete
desired nodes API »](delete-desired-nodes.md)

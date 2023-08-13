

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Migration APIs](migration-api.md)

[« Migration APIs](migration-api.md) [Feature migration APIs »](feature-
migration-api.md)

## 弃用信息接口

这些 API 专为 Kibana 的升级助手间接使用而设计。我们强烈建议您使用升级助手从 7.17 升级到 8.9.0。有关升级说明，请参阅升级到 Elastic8.9.0。

弃用 API 将用于检索有关不同群集、节点和索引级别设置的信息，这些设置使用将在将来版本中删除或更改的已弃用功能。

###Request

"获取/_migration/弃用"

'GET //<target>_migration/deprecations'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。

### 路径参数

`<target>`

    

(可选，字符串)要检查的数据流或索引的逗号分隔列表。支持通配符 ('*') 表达式。

指定此参数时，仅返回指定数据流或索引的弃用。

###Settings

您可以使用以下设置来控制弃用信息 API 的行为：

此设置专为 ElasticsearchService、Elastic Cloud Enterprise 和 ElasticCloud on Kubernetes 间接使用而设计。不支持直接使用。

"deprecation.skip_deprecated_settings"(动态) 默认为空列表。设置为弃用信息 API 要忽略的设置名称列表。API 不会返回与此列表中的设置相关的任何弃用。支持简单通配符匹配。

###Examples

若要查看群集中的违规者列表，请向"_migration/弃用"终结点提交 GET 请求：

    
    
    response = client.migration.deprecations
    puts response
    
    
    GET /_migration/deprecations

示例响应：

    
    
    {
      "cluster_settings" : [
        {
          "level" : "critical",
          "message" : "Cluster name cannot contain ':'",
          "url" : "https://www.elastic.co/guide/en/elasticsearch/reference/7.0/breaking-changes-7.0.html#_literal_literal_is_no_longer_allowed_in_cluster_name",
          "details" : "This cluster is named [mycompany:logging], which contains the illegal character ':'."
        }
      ],
      "node_settings" : [ ],
      "index_settings" : {
        "logs:apache" : [
          {
            "level" : "warning",
            "message" : "Index name cannot contain ':'",
            "url" : "https://www.elastic.co/guide/en/elasticsearch/reference/7.0/breaking-changes-7.0.html#_literal_literal_is_no_longer_allowed_in_index_name",
            "details" : "This index is named [logs:apache], which contains the illegal character ':'."
          }
        ]
      },
      "ml_settings" : [ ]
    }

响应会分解在升级群集之前应解决的所有特定向前不兼容设置。任何违规设置都表示为弃用警告。

下面是一个弃用警告示例：

    
    
    {
      "level" : "warning",
      "message" : "This is the generic descriptive message of the breaking change",
      "url" : "https://www.elastic.co/guide/en/elasticsearch/reference/6.0/breaking_60_indices_changes.html",
      "details" : "more information, like which nodes, indices, or settings are to blame"
    }

如图所示，有一个"级别"属性描述了问题的重要性。

warning

|

您可以直接升级，但您使用的是已弃用的功能，这些功能在未来版本中将不可用或行为不同。   ---|---关键

|

如果不解决此问题，则无法升级。   "message"属性和可选的"details"属性提供有关弃用警告的描述性信息。"url"属性提供指向中断性更改文档的链接，您可以在其中找到有关此更改的详细信息。

任何集群级别的弃用警告都可以在"cluster_settings"键下找到。同样，任何节点级警告都可以在"node_settings"下找到。由于只有选定的节点子集可能合并这些设置，因此请务必阅读"详细信息"部分，了解有关哪些节点受到影响的更多信息。索引警告按索引进行分区，可以使用查询中的索引模式进行筛选。本部分包括对请求路径中指定的数据流的支持索引的警告。可以在"ml_settings"键下找到与机器学习相关的弃用警告。

以下示例请求仅显示所有"logstash-*"索引的索引级弃用：

    
    
    response = client.migration.deprecations(
      index: 'logstash-*'
    )
    puts response
    
    
    GET /logstash-*/_migration/deprecations

[« Migration APIs](migration-api.md) [Feature migration APIs »](feature-
migration-api.md)

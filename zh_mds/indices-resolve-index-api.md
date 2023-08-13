

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Refresh API](indices-refresh.md) [Rollover API »](indices-rollover-
index.md)

## 解析索引接口

解析索引、别名和数据流的指定名称和/或索引模式。支持多种模式和远程集群。

    
    
    response = client.indices.resolve_index(
      name: 'my-index-*'
    )
    puts response
    
    
    GET /_resolve/index/my-index-*

###Request

'获取/_resolve/索引/<name>'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或索引别名具有"view_index_metadata"或"管理"索引权限。

### 路径参数

`<name>`

    

(必需，字符串)要解析的索引、别名和数据流的逗号分隔的名称或索引模式。可以使用"："语法指定远程群集上的资源<cluster><name>。

### 查询参数

`expand_wildcards`

    

(可选，字符串)通配符模式可以匹配的索引类型。如果请求可以以数据流为目标，则此参数确定通配符表达式是否与隐藏的数据流匹配。支持逗号分隔的值，例如"打开，隐藏"。有效值为：

`all`

     Match any data stream or index, including [hidden](api-conventions.html#multi-hidden "Hidden data streams and indices") ones. 
`open`

     Match open, non-hidden indices. Also matches any non-hidden data stream. 
`closed`

     Match closed, non-hidden indices. Also matches any non-hidden data stream. Data streams cannot be closed. 
`hidden`

     Match hidden data streams and hidden indices. Must be combined with `open`, `closed`, or both. 
`none`

     Wildcard patterns are not accepted. 

默认为"打开"。

###Examples

    
    
    response = client.indices.resolve_index(
      name: 'f*,remoteCluster1:bar*',
      expand_wildcards: 'all'
    )
    puts response
    
    
    GET /_resolve/index/f*,remoteCluster1:bar*?expand_wildcards=all

API 返回以下响应：

    
    
    {
      "indices": [                                 __{
          "name": "foo_closed",
          "attributes": [
            "closed" __]
        },
        {
          "name": "freeze-index",
          "aliases": [
            "f-alias"
          ],
          "attributes": [
            "open"
          ]
        },
        {
          "name": "remoteCluster1:bar-01",
          "attributes": [
            "open"
          ]
        }
      ],
      "aliases": [ __{
          "name": "f-alias",
          "indices": [
            "freeze-index",
            "my-index-000001"
          ]
        }
      ],
      "data_streams": [ __{
          "name": "foo",
          "backing_indices": [
            ".ds-foo-2099.03.07-000001"
          ],
          "timestamp_field": "@timestamp"
        }
      ]
    }

__

|

与提供的名称或表达式匹配的所有索引 ---|--- __

|

可能的索引属性包括"打开"、"关闭"、"隐藏"、"系统"和"冻结" __

|

与提供的名称或表达式匹配的所有别名 __

|

与提供的名称或表达式匹配的所有数据流 « 刷新 API 滚动更新 API »
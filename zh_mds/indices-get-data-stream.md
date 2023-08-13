

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Data stream APIs](data-stream-apis.md)

[« Delete data stream API](indices-delete-data-stream.md) [Migrate to data
stream API »](indices-migrate-to-data-stream.md)

## 获取数据流接口

检索有关一个或多个数据流的信息。请参阅获取有关数据流的信息。

    
    
    response = client.indices.get_data_stream(
      name: 'my-data-stream'
    )
    puts response
    
    
    GET /_data_stream/my-data-stream

###Request

"获取/_data_stream/<data-stream>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对数据流具有"view_index_metadata"或"管理"索引权限。

### 路径参数

`<data-stream>`

     (Optional, string) Comma-separated list of data stream names used to limit the request. Wildcard (`*`) expressions are supported. If omitted, all data streams will be returned. 

### 查询参数

`expand_wildcards`

    

(可选，字符串)通配符模式可以匹配的数据流类型。支持逗号分隔的值，例如"打开，隐藏"。有效值为：

"全部"、"隐藏"

     Match any data stream, including [hidden](api-conventions.html#multi-hidden "Hidden data streams and indices") ones. 
`open`, `closed`

     Matches any non-hidden data stream. Data streams cannot be closed. 
`none`

     Wildcard patterns are not accepted. 

默认为"打开"。

`include_defaults`

     (Optional, Boolean) Functionality in  [preview]  This functionality is in technical preview and may be changed or removed in a future release. Elastic will apply best effort to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.  . If `true`, return all default settings in the response. Defaults to `false`. 

### 响应正文

`data_streams`

    

(对象数组)包含有关检索到的数据流的信息。

"data_streams"中对象的属性

`name`

     (string) Name of the data stream. 
`timestamp_field`

    

(对象)包含有关数据流的"@timestamp"字段的信息。

"timestamp_field"的属性

`name`

     (string) Name of the data stream's timestamp field, which must be `@timestamp`. The `@timestamp` field must be included in every document indexed to the data stream. 

`indices`

    

(对象数组)包含有关数据流的支持索引的信息的对象数组。

此数组中的最后一项包含有关流的当前写入索引的信息。

"索引"对象的属性

`index_name`

     (string) Name of the backing index. For naming conventions, see [Generation](data-streams.html#data-streams-generation "Generation"). 
`index_uuid`

     (string) Universally unique identifier (UUID) for the index. 

`generation`

     (integer) Current [generation](data-streams.html#data-streams-generation "Generation") for the data stream. This number acts as a cumulative count of the stream's rollovers, starting at `1`. 
`_meta`

     (object) Custom metadata for the stream, copied from the `_meta` object of the stream's matching [index template](set-up-a-data-stream.html#create-index-template "Create an index template"). If empty, the response omits this property. 
`status`

    

(字符串)数据流的运行状况。

此运行状况基于流的支持索引的主分片和副本分片的状态。

"状态"的值

`GREEN`

     All shards are assigned. 
`YELLOW`

     All primary shards are assigned, but one or more replica shards are unassigned. 
`RED`

     One or more primary shards are unassigned, so some data is unavailable. 

`template`

    

(字符串)用于创建数据流的支持索引的索引模板的名称。

模板的索引模式必须与此数据流的名称匹配。请参阅创建索引模板。

`ilm_policy`

    

(字符串)流的匹配索引模板中当前 ILM 生命周期策略的名称。此生命周期策略在"索引.生命周期.名称"设置中设置。

如果模板不包含生命周期策略，则此属性不包含在响应中。

可以为数据流的后备索引分配不同的生命周期策略。要检索单个后备索引的生命周期策略，请使用 getindex 设置 API。

`hidden`

     (Boolean) If `true`, the data stream is [hidden](api-conventions.html#multi-hidden "Hidden data streams and indices"). 
`system`

     (Boolean) If `true`, the data stream is created and managed by an Elastic stack component and cannot be modified through normal user interaction. 
`allow_custom_routing`

     (Boolean) If `true`, the data stream this data stream allows custom routing on write request. 
`replicated`

     (Boolean) If `true`, the data stream is created and managed by cross-cluster replication and the local cluster can not write into this data stream or change its mappings. 
`lifecycle`

    

(对象)[预览版] 中的功能 此功能在技术预览版中，可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持约束。 .包含此数据流的数据生命周期管理的配置。

"生命周期"的属性

`data_retention`

     (string) If defined, every document added to this data stream will be stored at least for this time frame. Any time after this duration the document could be deleted. When empty, every document in this data stream will be stored indefinitely. 
`rollover`

     (object) The conditions which will trigger the rollover of a backing index as configured by the cluster setting `cluster.lifecycle.default.rollover`. This property is an implementation detail and it will only be retrieved when the query param `include_defaults` is set to `true`. The contents of this field are subject to change. 

###Examples

    
    
    response = client.indices.get_data_stream(
      name: 'my-data-stream*'
    )
    puts response
    
    
    GET _data_stream/my-data-stream*

API 返回以下响应：

    
    
    {
      "data_streams": [
        {
          "name": "my-data-stream",
          "timestamp_field": {
            "name": "@timestamp"
          },
          "indices": [
            {
              "index_name": ".ds-my-data-stream-2099.03.07-000001",
              "index_uuid": "xCEhwsp8Tey0-FLNFYVwSg"
            },
            {
              "index_name": ".ds-my-data-stream-2099.03.08-000002",
              "index_uuid": "PA_JquKGSiKcAKBA8DJ5gw"
            }
          ],
          "generation": 2,
          "_meta": {
            "my-meta-field": "foo"
          },
          "status": "GREEN",
          "template": "my-index-template",
          "ilm_policy": "my-lifecycle-policy",
          "hidden": false,
          "system": false,
          "allow_custom_routing": false,
          "replicated": false
        },
        {
          "name": "my-data-stream-two",
          "timestamp_field": {
            "name": "@timestamp"
          },
          "indices": [
            {
              "index_name": ".ds-my-data-stream-two-2099.03.08-000001",
              "index_uuid": "3liBu2SYS5axasRt6fUIpA"
            }
          ],
          "generation": 1,
          "_meta": {
            "my-meta-field": "foo"
          },
          "status": "YELLOW",
          "template": "my-index-template",
          "ilm_policy": "my-lifecycle-policy",
          "hidden": false,
          "system": false,
          "allow_custom_routing": false,
          "replicated": false
        }
      ]
    }

[« Delete data stream API](indices-delete-data-stream.md) [Migrate to data
stream API »](indices-migrate-to-data-stream.md)

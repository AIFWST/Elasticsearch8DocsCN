

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Transform APIs](transform-apis.md)

[« Get transform statistics API](get-transform-stats.md) [Reset transform
API »](reset-transform.md)

## 预览转换接口

预览转换。

###Request

"得到_transform/<transform_id>/_preview"

"发布_transform/<transform_id>/_preview"

"得到_transform/_preview"

"发布_transform/_preview"

###Prerequisites

需要以下权限：

* 集群："manage_transform"("transform_admin"内置角色授予此权限) * 源索引："读取"、"view_index_metadata"。

###Description

此 API 生成结果的预览，当您使用相同的配置运行创建转换 API 时，您将获得这些结果。它最多返回 100 个结果。计算基于源索引中的所有当前数据。

它还为目标索引生成映射和设置的列表。如果启动转换时目标索引不存在，则这些是使用的映射和设置。这些值是根据源索引和转换聚合的字段类型确定的。

有一些限制可能会导致映射不佳。解决方法是，在开始转换之前，使用首选映射创建目标索引或索引模板。

必须为转换选择"最新"或"透视"方法;不能在单个转换中同时使用两者。

预览转换时，它会使用调用 API 的用户的凭据。启动转换时，它会使用最后一个用户的角色来创建或更新转换。如果两组角色不同，预览可能无法准确反映转换的行为。为避免此类问题，创建或更新转换的同一用户应预览转换，以确保它返回预期数据。或者，使用辅助授权标头来提供凭据

### 路径参数

`<transform_id>`

    

(可选，字符串)要预览的转换的 ID。

如果提供 '<transform_id>' 作为路径参数，则无法在请求正文中提供转换配置详细信息。

### 查询参数

`timeout`

     (Optional, time) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 请求正文

`description`

     (Optional, string) Free text description of the transform. 

`dest`

    

(可选，对象)转换的目标。

"目标"的属性

`index`

     (Optional, string) The _destination index_ for the transform. 

在"透视"转换的情况下，尽可能根据源字段推导目标索引的映射。如果需要备用映射，请在开始转换之前使用创建索引 API。

在"最新"转换的情况下，永远不会推断映射。如果不需要目标索引的动态映射，请在启动转换之前使用 Createindex API。

`pipeline`

     (Optional, string) The unique identifier for an [ingest pipeline](ingest.html "Ingest pipelines"). 

`frequency`

     (Optional, [time units](api-conventions.html#time-units "Time units")) The interval between checks for changes in the source indices when the transform is running continuously. The minimum value is `1s` and the maximum is `1h`. The default value is `1m`. 

`latest`

    

(必填*，对象)"latest"方法通过查找每个唯一键的最新文档来转换数据。

"最新"的属性

`sort`

     (Required, string) Specifies the date field that is used to identify the latest documents. 
`unique_key`

     (Required, array of strings) Specifies an array of one or more fields that are used to group the data. 

`pivot`

    

(必填，对象)"透视"方法通过聚合和分组数据来转换数据。这些对象定义"分组依据"字段和聚合以减少数据。

"枢轴"的属性

"聚合"或"聚合"

    

(必填，对象)定义如何聚合分组数据。目前支持以下聚合：

* 平均值 * 存储桶脚本 * 存储桶选择器 * 基数 * 过滤器 * 地理边界 * 地理质心 * 地理线 * 笛卡尔边界 * 笛卡尔质心 * 最大值 * 中位数绝对偏差 * 最小值 * 缺失 * 百分位数 * 范围 * 稀有术语 * 脚本化指标 * 统计数据 * 总和 * 条款 * 热门指标 * 值计数 * 加权平均值

`group_by`

    

(必填，对象)定义如何对数据进行分组。每个透视可以定义多个分组。目前支持以下分组：

* 日期直方图 * 地瓦网格 * 直方图 * 术语

分组属性可以选择具有"missing_bucket"属性。Ifit的"true"，在相应的"group_by"字段中没有值的文档包括在内。默认为"假"。

`retention_policy`

    

(可选，对象)定义转换的保留策略。满足定义条件的数据将从目标索引中删除。

"retention_policy"的属性

`time`

    

(必填，对象)指定转换使用时间字段来设置保留策略。如果保留策略的"time.field"存在并且包含早于"max.age"的数据，则会删除数据。

"时间"的属性

`field`

     (Required, string) The date field that is used to calculate the age of the document. Set `time.field` to an existing date field. 
`max_age`

     (Required, [time units](api-conventions.html#time-units "Time units")) Specifies the maximum age of a document in the destination index. Documents that are older than the configured value are removed from the destination index. 

`source`

    

(必填，对象)转换的数据源。

"源"的属性

`index`

    

(必需，字符串或数组)转换的_source indices_。它可以是单个索引、索引模式(例如，"my-index-*")、索引数组(例如，"["my-index-000001"、"my-index-000002"]')或索引模式数组(例如，"["my-index-*"、"my-other-index-*"]')。对于远程索引，使用语法"remote_name：index_name""。

如果任何索引位于远程集群中，则主节点和至少一个转换节点必须具有"remote_cluster_client"节点角色。

`query`

     (Optional, object) A query clause that retrieves a subset of data from the source index. See [Query DSL](query-dsl.html "Query DSL"). 
`runtime_mappings`

     (Optional, object) Definitions of search-time runtime fields that can be used by the transform. For search runtime fields all data nodes, including remote nodes, must be 7.12 or later. 

`sync`

    

(可选，对象)定义转换连续运行所需的属性。

"同步"的属性

`time`

    

(可选，对象)指定转换使用时间字段来同步源索引和目标索引。

"时间"的属性

`delay`

     (Optional, [time units](api-conventions.html#time-units "Time units")) The time delay between the current time and the latest input data time. The default value is `60s`. 
`field`

     (Optional, string) The date field that is used to identify new documents in the source. 

`settings`

    

(可选，对象)定义可选的转换设置。

"设置"的属性

`align_checkpoints`

     (Optional, boolean) Specifies whether the transform checkpoint ranges should be optimized for performance. Such optimization can align checkpoint ranges with date histogram interval when date histogram is specified as a group source in the transform config. As an effect, less document updates in the destination index will be performed thus improving overall performance. The default value is `true`, which means the checkpoint ranges will be optimized if possible. 
`dates_as_epoch_millis`

     (Optional, boolean) Defines if dates in the output should be written as ISO formatted string (default) or as millis since epoch. `epoch_millis` has been the default for transforms created before version `7.11`. For compatible output set this to `true`. The default value is `false`. 
`deduce_mappings`

     (Optional, boolean) Specifies whether the transform should deduce the destination index mappings from the transform config. The default value is `true`, which means the destination index mappings will be deduced if possible. 
`docs_per_second`

     (Optional, float) Specifies a limit on the number of input documents per second. This setting throttles the transform by adding a wait time between search requests. The default value is `null`, which disables throttling. 
`max_page_search_size`

     (Optional, integer) Defines the initial page size to use for the composite aggregation for each checkpoint. If circuit breaker exceptions occur, the page size is dynamically adjusted to a lower value. The minimum value is `10` and the maximum is `65,536`. The default value is `500`. 
`unattended`

     (Optional, boolean) If `true`, the transform runs in unattended mode. In unattended mode, the transform retries indefinitely in case of an error which means the transform never fails. Setting the number of retries other than infinite fails in validation. Defaults to `false`. 

### 响应正文

`generated_dest_index`

    

(对象)包含有关目标索引的详细信息。

"generated_dest_index"的属性

`aliases`

     (object) The aliases for the destination index. 
`mappings`

     (object) The [mappings](mapping.html "Mapping") for each document in the destination index. 
`settings`

     (object) The [index settings](index-modules.html#index-modules-settings "Index Settings") for the destination index. 

`preview`

     (array) An array of documents. In particular, they are the JSON representation of the documents that would be created in the destination index by the transform. 

###Examples

    
    
    POST _transform/_preview
    {
      "source": {
        "index": "kibana_sample_data_ecommerce"
      },
      "pivot": {
        "group_by": {
          "customer_id": {
            "terms": {
              "field": "customer_id",
              "missing_bucket": true
            }
          }
        },
        "aggregations": {
          "max_price": {
            "max": {
              "field": "taxful_total_price"
            }
          }
        }
      }
    }

此示例返回的数据如下所示：

    
    
    {
      "preview" : [
        {
          "max_price" : 171.0,
          "customer_id" : "10"
        },
        {
          "max_price" : 233.0,
          "customer_id" : "11"
        },
        {
          "max_price" : 200.0,
          "customer_id" : "12"
        }
        ...
      ],
      "generated_dest_index" : {
        "mappings" : {
          "_meta" : {
            "_transform" : {
              "transform" : "transform-preview",
              "version" : {
                "created" : "7.7.0"
              },
              "creation_date_in_millis" : 1584738236757
            },
            "created_by" : "transform"
          },
          "properties" : {
            "max_price" : {
              "type" : "half_float"
            },
            "customer_id" : {
              "type" : "keyword"
            }
          }
        },
        "settings" : {
          "index" : {
            "number_of_shards" : "1",
            "auto_expand_replicas" : "0-1"
          }
        },
        "aliases" : { }
      }
    }

[« Get transform statistics API](get-transform-stats.md) [Reset transform
API »](reset-transform.md)

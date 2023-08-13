

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Transform APIs](transform-apis.md)

[« Transform APIs](transform-apis.md) [Delete transform API »](delete-
transform.md)

## 创建转换接口

实例化转换。

###Request

"放_transform/<transform_id>"

###Prerequisites

需要以下权限：

* 集群："manage_transform"("transform_admin"内置角色授予此权限) * 源索引："读取"、"view_index_metadata" * 目标索引："读取"、"create_index"、"索引"。如果配置了"retention_policy"，则还需要"删除"权限。

###Description

此 API 定义一个转换，该转换从源索引复制数据，对其进行转换，并将其保存到以实体为中心的目标索引中。如果选择对转换使用 pivot 方法，则实体由"透视"对象中的一组"group_by"字段定义。如果选择使用最新方法，则实体由"latest"对象中的"unique_key"字段值定义。

还可以将目标索引视为二维表格数据结构(称为数据框)。数据框中每个文档的 ID 是根据实体的哈希生成的，因此每个实体都有一个唯一的行。有关详细信息，请参阅_Transforming data_。

创建转换时，将进行一系列验证以确保其成功。例如，检查源索引是否存在，并检查目标索引是否不是源索引模式的一部分。您可以使用"defer_validation"参数跳过这些检查。

延迟验证始终在转换启动时运行，但权限检查除外。

* 转换会记住创建它的用户在创建时具有哪些角色，并使用这些相同的角色。如果这些角色对源索引和目标索引没有所需的特权，则转换在尝试未经授权的操作时将失败。如果提供辅助授权标头，则改用这些凭据。  * 您必须使用 Kibana 或此 API 来创建转换。不要使用 Elasticsearch 索引 API 将转换直接添加到任何 '.transform-internal*' 索引中。如果启用了 Elasticsearch 安全功能，请不要授予用户任何对 '.transform-internal*' 索引的权限。如果您使用的是 7.5 之前的转换，也不要授予用户对".data-frame-internal*"索引的任何权限。

必须为转换选择最新方法或透视方法;不能在单个转换中同时使用两者。

### 路径参数

`<transform_id>`

     (Required, string) Identifier for the transform. This identifier can contain lowercase alphanumeric characters (a-z and 0-9), hyphens, and underscores. It has a 64 character limit and must start and end with alphanumeric characters. 

### 查询参数

`defer_validation`

     (Optional, Boolean) When `true`, deferrable validations are not run. This behavior may be desired if the source index does not exist until after the transform is created. 
`timeout`

     (Optional, time) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 请求正文

`description`

     (Optional, string) Free text description of the transform. 

`dest`

    

(必填，对象)转换的目标。

"目标"的属性

`index`

     (Required, string) The _destination index_ for the transform. 

在"透视"转换的情况下，尽可能根据源字段推导目标索引的映射。如果需要备用映射，请在开始转换之前使用创建索引 API。

在"最新"转换的情况下，永远不会推断映射。如果不需要目标索引的动态映射，请在启动转换之前使用 Createindex API。

`aliases`

     (Optional, array of objects) The aliases that the destination index for the transform should have. Aliases are manipulated using the stored credentials of the transform, which means the secondary credentials supplied at creation time (if both primary and secondary credentials are specified). 

目标索引将添加到别名中，无论目标索引是由转换创建的还是由用户预先创建的。

\+ ."别名"的属性

Details

`alias`

     (Required, string) The name of the alias. 
`move_on_creation`

     (Optional, boolean) Whether or not the destination index should be the **only** index in this alias. If `true`, all the other indices will be removed from this alias before adding the destination index to this alias. Defaults to `false`. 

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

`_meta`

     (Optional, object) Defines optional transform metadata. 

`pivot`

    

(必填*，对象)"透视"方法通过聚合和分组数据来转换数据。这些对象定义"分组依据"字段和聚合以减少数据。

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
`num_failure_retries`

     (Optional, integer) Defines the number of retries on a recoverable failure before the transform task is marked as `failed`. The minimum value is `0` and the maximum is `100`. `-1` can be used to denote infinity. In this case, the transform never gives up on retrying a recoverable failure. The default value is the cluster-level setting `num_transform_failure_retries`. 
`unattended`

     (Optional, boolean) If `true`, the transform runs in unattended mode. In unattended mode, the transform retries indefinitely in case of an error which means the transform never fails. Setting the number of retries other than infinite fails in validation. Defaults to `false`. 

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

    

(必填，对象)指定转换使用时间字段来同步源索引和目标索引。

"时间"的属性

`delay`

     (Optional, [time units](api-conventions.html#time-units "Time units")) The time delay between the current time and the latest input data time. The default value is `60s`. 
`field`

    

(必需，字符串)用于标识源中的新文档的日期字段。

强烈建议使用包含摄取时间戳的字段。如果使用其他字段，则可能需要设置"延迟"，以便它考虑数据传输延迟。

###Examples

以下转换使用"透视"方法：

    
    
    PUT _transform/ecommerce_transform1
    {
      "source": {
        "index": "kibana_sample_data_ecommerce",
        "query": {
          "term": {
            "geoip.continent_name": {
              "value": "Asia"
            }
          }
        }
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
      },
      "description": "Maximum priced ecommerce data by customer_id in Asia",
      "dest": {
        "index": "kibana_sample_data_ecommerce_transform1",
        "pipeline": "add_timestamp_pipeline"
      },
      "frequency": "5m",
      "sync": {
        "time": {
          "field": "order_date",
          "delay": "60s"
        }
      },
      "retention_policy": {
        "time": {
          "field": "order_date",
          "max_age": "30d"
        }
      }
    }

创建转换时，您会收到以下结果：

    
    
    {
      "acknowledged" : true
    }

以下转换使用"最新"方法：

    
    
    PUT _transform/ecommerce_transform2
    {
      "source": {
        "index": "kibana_sample_data_ecommerce"
      },
      "latest": {
        "unique_key": ["customer_id"],
        "sort": "order_date"
      },
      "description": "Latest order for each customer",
      "dest": {
        "index": "kibana_sample_data_ecommerce_transform2"
      },
      "frequency": "5m",
      "sync": {
        "time": {
          "field": "order_date",
          "delay": "60s"
        }
      }
    }

[« Transform APIs](transform-apis.md) [Delete transform API »](delete-
transform.md)

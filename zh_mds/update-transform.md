

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Transform APIs](transform-apis.md)

[« Stop transforms API](stop-transform.md) [Upgrade transforms API
»](upgrade-transforms.md)

## 更新转换接口

更新转换的某些属性。

###Request

"发布_transform/<transform_id>/_update"

###Prerequisites

需要以下权限：

* 集群："manage_transform"("transform_admin"内置角色授予此权限) * 源索引："读取"、"view_index_metadata" * 目标索引："读取"、"索引"。如果配置了"retention_policy"，则还需要"删除"索引权限。

###Description

此 API 更新现有转换。可以更新的属性列表是创建转换时可以定义的列表的子集。

更新转换时，将进行一系列验证以确保其成功。您可以使用"defer_validation"参数跳过这些检查。

除说明之外的所有更新属性在转换启动下一个检查点之前不会生效。因此，每个检查点都有数据一致性。

* 转换会记住更新转换的用户在更新时具有哪些角色，并使用这些权限运行。如果提供辅助授权标头，则改用这些凭据。  * 您必须使用 Kibana 或此 API 来更新转换。不支持直接更新任何转换内部索引、系统索引或隐藏索引，这可能会导致永久性失败。

### 路径参数

`<transform_id>`

     (Required, string) Identifier for the transform. 

### 查询参数

`defer_validation`

     (Optional, Boolean) When `true`, deferrable validations are not run. This behavior may be desired if the source index does not exist until after the transform is updated. 
`timeout`

     (Optional, time) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 请求正文

`description`

     (Optional, string) Free text description of the transform. 

`dest`

    

(可选，对象)转换的目标。

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

`_meta`

     (Optional, object) Defines optional transform metadata. 

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

    

(可选，对象)转换的数据源。

"源"的属性

`index`

    

(必需，字符串或数组)转换的_source indices_。它可以是单个索引、索引模式(例如，"my-index-*")、索引数组(例如，"["my-index-000001"、"my-index-000002"]')或索引模式数组(例如，"["my-index-*"、"my-other-index-*"]')。对于远程索引，使用语法"remote_name：index_name""。

如果任何索引位于远程集群中，则主节点和至少一个转换节点必须具有"remote_cluster_client"节点角色。

`query`

     (Optional, object) A query clause that retrieves a subset of data from the source index. See [Query DSL](query-dsl.html "Query DSL"). 

`sync`

    

(可选，对象)定义转换连续运行所需的属性。

仅当这些属性是连续转换时，才能更新这些属性。不能将批量转换更改为连续转换，反之亦然。相反，请在 Kibana 中克隆转换并添加或删除"sync"属性。

"同步"的属性

`time`

    

(必填，对象)指定转换使用时间字段来同步源索引和目标索引。

"时间"的属性

`delay`

     (Optional, [time units](api-conventions.html#time-units "Time units")) The time delay between the current time and the latest input data time. The default value is `60s`. 
`field`

    

(必需，字符串)用于标识源中的新文档的日期字段。

通常，最好使用包含引入时间戳的字段。如果使用其他字段，则可能需要设置"延迟"，以便它考虑数据传输延迟。

###Examples

    
    
    response = client.transform.update_transform(
      transform_id: 'simple-kibana-ecomm-pivot',
      body: {
        source: {
          index: 'kibana_sample_data_ecommerce',
          query: {
            term: {
              "geoip.continent_name": {
                value: 'Asia'
              }
            }
          }
        },
        description: 'Maximum priced ecommerce data by customer_id in Asia',
        dest: {
          index: 'kibana_sample_data_ecommerce_transform_v2',
          pipeline: 'add_timestamp_pipeline'
        },
        frequency: '15m',
        sync: {
          time: {
            field: 'order_date',
            delay: '120s'
          }
        }
      }
    )
    puts response
    
    
    POST _transform/simple-kibana-ecomm-pivot/_update
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
      "description": "Maximum priced ecommerce data by customer_id in Asia",
      "dest": {
        "index": "kibana_sample_data_ecommerce_transform_v2",
        "pipeline": "add_timestamp_pipeline"
      },
      "frequency": "15m",
      "sync": {
        "time": {
          "field": "order_date",
          "delay": "120s"
        }
      }
    }

更新转换后，您会收到更新的配置：

    
    
    {
      "id" : "simple-kibana-ecomm-pivot",
      "authorization" : {
        "roles" : [
          "superuser"
        ]
      },
      "version" : "8.4.0",
      "create_time" : 1656113450613,
      "source" : {
        "index" : [
          "kibana_sample_data_ecommerce"
        ],
        "query" : {
          "term" : {
            "geoip.continent_name" : {
              "value" : "Asia"
            }
          }
        }
      },
      "dest" : {
        "index" : "kibana_sample_data_ecommerce_transform_v2",
        "pipeline" : "add_timestamp_pipeline"
      },
      "frequency" : "15m",
      "sync" : {
        "time" : {
          "field" : "order_date",
          "delay" : "120s"
        }
      },
      "pivot" : {
        "group_by" : {
          "customer_id" : {
            "terms" : {
              "field" : "customer_id"
            }
          }
        },
        "aggregations" : {
          "max_price" : {
            "max" : {
              "field" : "taxful_total_price"
            }
          }
        }
      },
      "description" : "Maximum priced ecommerce data by customer_id in Asia",
      "settings" : { }
    }

[« Stop transforms API](stop-transform.md) [Upgrade transforms API
»](upgrade-transforms.md)

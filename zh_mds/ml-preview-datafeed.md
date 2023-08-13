

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Post data to jobs API](ml-post-data.md) [Reset anomaly detection jobs API
»](ml-reset-job.md)

## 预览数据馈送接口

预览数据馈送。

###Request

"获取_ml/数据馈送/<datafeed_id>/_preview"

"发布_ml/数据馈送/<datafeed_id>/_preview"

"获取_ml/数据馈送/_preview"

"发布_ml/数据馈送/_preview"

###Prerequisites

需要以下权限：

* 集群："manage_ml"("machine_learning_admin"内置角色授予此权限) * 在数据源中配置的源索引："读取"。

###Description

预览数据馈送 API 从数据馈送返回搜索结果的第一"页"。您可以在 API 中预览现有数据馈送或提供数据馈送和异常情况检测作业的配置详细信息。预览显示将传递到异常情况检测引擎的数据的结构。

启用 Elasticsearch 安全功能后，将使用调用预览数据馈送 API 的用户的凭据预览数据馈送查询。启动数据馈送时，它使用最后一个用户的角色运行查询以创建或更新查询。如果两组角色不同，则预览可能无法准确反映数据馈送在启动时将返回的内容。为避免此类问题，创建或更新数据馈送的同一用户应预览它以确保它返回预期数据。或者，使用辅助授权标头来提供凭据。

### 路径参数

`<datafeed_id>`

    

(可选，字符串)唯一标识数据馈送的数字字符串。此标识符可以包含小写字母数字字符 (a-zand 0-9)、连字符和下划线。它必须以字母数字字符开头和结尾。

如果提供"<datafeed_id>"作为路径参数，则无法在请求正文中提供数据馈送或异常情况检测作业配置详细信息。

### 查询参数

`end`

    

(可选，字符串)数据馈送预览应结束的时间。预览可能不会转到所提供值的末尾，因为仅返回结果的第一页。可以使用下列格式之一指定时间：

* 带毫秒的 ISO 8601 格式，例如"2017-01-22T06：00：00.000Z" * 不含毫秒的 ISO 8601 格式，例如"2017-01-22T06：00：00+00：00" * 自纪元以来的毫秒，例如"1485061200000"

使用 ISO 8601 格式之一的日期时间参数必须具有时区指示符，其中"Z"被接受为 UTC 时间的缩写。

当需要 URL 时(例如，在浏览器中)，时区指示符中使用的"+"必须编码为"%2B"。

此值是独占的。

`start`

     (Optional, string) The time that the datafeed preview should begin, which can be specified by using the same formats as the `end` parameter. This value is inclusive. 

如果未提供"start"或"end"参数，则 datafeedpreview 将搜索整个数据时间，但排除"冷"或"冻结"数据层中的数据。

### 请求正文

`datafeed_config`

     (Optional, object) The datafeed definition to preview. For valid definitions, see the [create datafeeds API](ml-put-datafeed.html#ml-put-datafeed-request-body "Request body"). 
`job_config`

     (Optional, object) The configuration details for the anomaly detection job that is associated with the datafeed. If the `datafeed_config` object does not include a `job_id` that references an existing anomaly detection job, you must supply this `job_config` object. If you include both a `job_id` and a `job_config`, the latter information is used. You cannot specify a `job_config` object unless you also supply a `datafeed_config` object. For valid definitions, see the [create anomaly detection jobs API](ml-put-job.html#ml-put-job-request-body "Request body"). 

###Examples

以下是提供现有数据馈送 ID 的示例：

    
    
    response = client.ml.preview_datafeed(
      datafeed_id: 'datafeed-high_sum_total_sales'
    )
    puts response
    
    
    GET _ml/datafeeds/datafeed-high_sum_total_sales/_preview

此示例返回的数据如下所示：

    
    
    [
      {
        "order_date" : 1574294659000,
        "category.keyword" : "Men's Clothing",
        "customer_full_name.keyword" : "Sultan Al Benson",
        "taxful_total_price" : 35.96875
      },
      {
        "order_date" : 1574294918000,
        "category.keyword" : [
          "Women's Accessories",
          "Women's Clothing"
        ],
        "customer_full_name.keyword" : "Pia Webb",
        "taxful_total_price" : 83.0
      },
      {
        "order_date" : 1574295782000,
        "category.keyword" : [
          "Women's Accessories",
          "Women's Shoes"
        ],
        "customer_full_name.keyword" : "Brigitte Graham",
        "taxful_total_price" : 72.0
      }
    ]

以下示例在 API 中提供数据馈送和异常情况检测作业配置详细信息：

    
    
    response = client.ml.preview_datafeed(
      body: {
        datafeed_config: {
          indices: [
            'kibana_sample_data_ecommerce'
          ],
          query: {
            bool: {
              filter: [
                {
                  term: {
                    _index: 'kibana_sample_data_ecommerce'
                  }
                }
              ]
            }
          },
          scroll_size: 1000
        },
        job_config: {
          description: 'Find customers spending an unusually high amount in an hour',
          analysis_config: {
            bucket_span: '1h',
            detectors: [
              {
                detector_description: 'High total sales',
                function: 'high_sum',
                field_name: 'taxful_total_price',
                over_field_name: 'customer_full_name.keyword'
              }
            ],
            influencers: [
              'customer_full_name.keyword',
              'category.keyword'
            ]
          },
          analysis_limits: {
            model_memory_limit: '10mb'
          },
          data_description: {
            time_field: 'order_date',
            time_format: 'epoch_ms'
          }
        }
      }
    )
    puts response
    
    
    POST _ml/datafeeds/_preview
    {
      "datafeed_config": {
        "indices" : [
          "kibana_sample_data_ecommerce"
        ],
        "query" : {
          "bool" : {
            "filter" : [
              {
                "term" : {
                  "_index" : "kibana_sample_data_ecommerce"
                }
              }
            ]
          }
        },
        "scroll_size" : 1000
      },
      "job_config": {
        "description" : "Find customers spending an unusually high amount in an hour",
        "analysis_config" : {
          "bucket_span" : "1h",
          "detectors" : [
            {
              "detector_description" : "High total sales",
              "function" : "high_sum",
              "field_name" : "taxful_total_price",
              "over_field_name" : "customer_full_name.keyword"
            }
          ],
          "influencers" : [
            "customer_full_name.keyword",
            "category.keyword"
          ]
        },
        "analysis_limits" : {
          "model_memory_limit" : "10mb"
        },
        "data_description" : {
          "time_field" : "order_date",
          "time_format" : "epoch_ms"
        }
      }
    }

此示例返回的数据如下所示：

    
    
    [
      {
        "order_date" : 1574294659000,
        "category.keyword" : "Men's Clothing",
        "customer_full_name.keyword" : "Sultan Al Benson",
        "taxful_total_price" : 35.96875
      },
      {
        "order_date" : 1574294918000,
        "category.keyword" : [
          "Women's Accessories",
          "Women's Clothing"
        ],
        "customer_full_name.keyword" : "Pia Webb",
        "taxful_total_price" : 83.0
      },
      {
        "order_date" : 1574295782000,
        "category.keyword" : [
          "Women's Accessories",
          "Women's Shoes"
        ],
        "customer_full_name.keyword" : "Brigitte Graham",
        "taxful_total_price" : 72.0
      }
    ]

[« Post data to jobs API](ml-post-data.md) [Reset anomaly detection jobs API
»](ml-reset-job.md)

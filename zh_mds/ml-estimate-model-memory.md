

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Delete expired data API](ml-delete-expired-data.md) [Flush jobs API
»](ml-flush-job.md)

## 估计异常检测作业模型内存API

估计异常情况检测作业模型的内存使用情况。它基于作业的分析配置详细信息和它引用的字段的基数估计值。

###Request

"发布 _ml/anomaly_detectors/_estimate_model_memory"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

### 请求正文

`analysis_config`

     (Required, object) For a list of the properties that you can specify in the `analysis_config` component of the body of this API, see [`analysis_config`](ml-put-job.html#put-analysisconfig). 
`max_bucket_cardinality`

     (Required*, object) Estimates of the highest cardinality in a single bucket that is observed for influencer fields over the time period that the job analyzes data. To produce a good answer, values must be provided for all influencer fields. Providing values for fields that are not listed as `influencers` has no effect on the estimation.  
*It can be omitted from the request if there are no `influencers`. 
`overall_cardinality`

     (Required*, object) Estimates of the cardinality that is observed for fields over the whole time period that the job analyzes data. To produce a good answer, values must be provided for fields referenced in the `by_field_name`, `over_field_name` and `partition_field_name` of any detectors. Providing values for other fields has no effect on the estimation.  
*It can be omitted from the request if no detectors have a `by_field_name`, `over_field_name` or `partition_field_name`. 

###Examples

    
    
    response = client.ml.estimate_model_memory(
      body: {
        analysis_config: {
          bucket_span: '5m',
          detectors: [
            {
              function: 'sum',
              field_name: 'bytes',
              by_field_name: 'status',
              partition_field_name: 'app'
            }
          ],
          influencers: [
            'source_ip',
            'dest_ip'
          ]
        },
        overall_cardinality: {
          status: 10,
          app: 50
        },
        max_bucket_cardinality: {
          source_ip: 300,
          dest_ip: 30
        }
      }
    )
    puts response
    
    
    POST _ml/anomaly_detectors/_estimate_model_memory
    {
      "analysis_config": {
        "bucket_span": "5m",
        "detectors": [
          {
            "function": "sum",
            "field_name": "bytes",
            "by_field_name": "status",
            "partition_field_name": "app"
          }
        ],
        "influencers": [ "source_ip", "dest_ip" ]
      },
      "overall_cardinality": {
        "status": 10,
        "app": 50
      },
      "max_bucket_cardinality": {
        "source_ip": 300,
        "dest_ip": 30
      }
    }

估计值返回以下结果：

    
    
    {
      "model_memory_estimate": "21mb"
    }

[« Delete expired data API](ml-delete-expired-data.md) [Flush jobs API
»](ml-flush-job.md)

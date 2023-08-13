

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Get model snapshots API](ml-get-snapshot.md) [Get overall buckets API
»](ml-get-overall-buckets.md)

## 获取异常检测作业模型快照升级统计信息API

检索异常情况检测作业模型快照升级的使用情况信息。

###Request

'GET_ml/anomaly_detectors/<job_id>/model_snapshots/<snapshot_id>/_upgrade/_stats"

'GET_ml/anomaly_detectors<job_id>/，<job_id>/model_snapshots/_all/_upgrade/_stats"

"获取_ml/anomaly_detectors/_all/model_snapshots/_all/_upgrade/_stats"

###Prerequisites

需要"monitor_ml"群集权限。此权限包含在"machine_learning_user"内置角色中。

###Description

异常情况检测作业模型快照升级是短暂的。仅返回调用此 API 时正在进行的升级。

### 路径参数

`<job_id>`

     (string) Identifier for the anomaly detection job. It can be a job identifier, a group name, or a wildcard expression. 
`<snapshot_id>`

    

(字符串)模型快照的标识符。

您可以使用以逗号分隔的快照 ID 列表在单个 API 请求中获取多个异常情况检测作业模型快照升级的统计信息。您还可以使用通配符表达式或"_all"。

### 查询参数

`allow_no_match`

    

(可选，布尔值)指定在请求时要执行的操作：

* 包含通配符表达式，并且没有匹配的作业。  * 包含"_all"字符串或不包含标识符，并且没有匹配项。  * 包含通配符表达式，并且只有部分匹配。

默认值为"true"，当没有匹配项时，它将返回一个空的"jobs"数组，当存在部分匹配时，它将返回结果的子集。如果此参数为"false"，则当没有匹配项或只有部分匹配项时，请求将返回"404"状态代码。

### 响应正文

API 返回异常情况检测作业模型快照升级状态对象的数组。所有这些属性都是信息性的;您无法更新其值。

`assignment_explanation`

     (string) For started datafeeds only, contains messages relating to the selection of a node. 
`job_id`

     (string) Identifier for the anomaly detection job. 
`node`

    

(对象)包含运行升级任务的节点的属性。此信息仅适用于分配给节点的升级任务。

Details

`attributes`

     (object) Lists node attributes such as `ml.machine_memory` or `ml.max_open_jobs` settings. 
`ephemeral_id`

     (string) The ephemeral ID of the node. 
`id`

     (string) The unique identifier of the node. 
`name`

     (string) The node name. For example, `0-o0tOo`. 
`transport_address`

     (string) The host and port where transport HTTP connections are accepted. 

`snapshot_id`

     (string) A numerical character string that uniquely identifies the model snapshot. For example, `1575402236000`. 
`state`

     (string) One of `loading_old_state`, `saving_new_state`, `stopped` or `failed`. 

### 响应码

"404"(缺少资源)

     If `allow_no_match` is `false`, this code indicates that there are no resources that match the request or only partial matches for the request. 

###Examples

    
    
    response = client.ml.get_model_snapshot_upgrade_stats(
      job_id: 'low_request_rate',
      snapshot_id: '_all'
    )
    puts response
    
    
    GET _ml/anomaly_detectors/low_request_rate/model_snapshots/_all/_upgrade/_stats

API 返回以下结果：

    
    
    {
      "count" : 1,
      "model_snapshot_upgrades" : [
        {
          "job_id" : "low_request_rate",
          "snapshot_id" : "1828371",
          "state" : "saving_new_state",
          "node" : {
            "id" : "7bmMXyWCRs-TuPfGJJ_yMw",
            "name" : "node-0",
            "ephemeral_id" : "hoXMLZB0RWKfR9UPPUCxXX",
            "transport_address" : "127.0.0.1:9300",
            "attributes" : {
              "ml.machine_memory" : "17179869184",
              "ml.max_open_jobs" : "512"
            }
          },
          "assignment_explanation" : ""
        }
      ]
    }

[« Get model snapshots API](ml-get-snapshot.md) [Get overall buckets API
»](ml-get-overall-buckets.md)

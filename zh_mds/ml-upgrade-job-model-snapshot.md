

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Update model snapshots API](ml-update-snapshot.md) [Machine learning data
frame analytics APIs »](ml-df-analytics-apis.md)

## 升级模型快照接口

将异常情况检测模型快照升级到最新的主要版本。

###Request

"发布 _ml/anomaly_detectors/<job_id>/model_snapshots/<snapshot_id>/_upgrade"

###Prerequisites

* 需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。  * 升级后的快照必须具有与之前主要版本匹配的版本。  * 升级后的快照不得是当前的异常情况检测作业快照。

###Description

随着时间的推移，较旧的快照格式将被弃用和删除。异常检测作业仅支持来自当前或以前主要版本的快照。

此 API 提供了一种将快照升级到当前主要版本的方法。这有助于为群集升级到下一个主要版本做好准备。

每个异常情况检测作业一次只能升级一个快照，并且升级后的快照不能是异常情况检测作业的当前快照。

### 路径参数

`<job_id>`

     (Required, string) Identifier for the anomaly detection job. 
`<snapshot_id>`

     (Required, string) Identifier for the model snapshot. 

### 查询参数

`timeout`

     (Optional, time) Controls the time to wait for the request to complete. The default value is 30 minutes. 
`wait_for_completion`

     (Optional, boolean) When true, the API won't respond until the upgrade is complete. Otherwise, it responds as soon as the upgrade task is assigned to a node. Default is false. 

### 响应正文

`node`

     (string) The ID of the assigned node for the upgrade task if it is still running. 
`completed`

     (boolean) When true, this means the task is complete. When false, it is still running. 

###Examples

    
    
    POST _ml/anomaly_detectors/low_request_rate/model_snapshots/1828371/_upgrade?timeout=45m&wait_for_completion=true

快照升级开始时，您会收到以下结果：

    
    
    {
      "completed" : false,
      "node" : "node-1"
    }

[« Update model snapshots API](ml-update-snapshot.md) [Machine learning data
frame analytics APIs »](ml-df-analytics-apis.md)

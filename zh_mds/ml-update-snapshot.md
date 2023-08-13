

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Update anomaly detection jobs API](ml-update-job.md) [Upgrade model
snapshots API »](ml-upgrade-job-model-snapshot.md)

## 更新模型快照API

更新快照的某些属性。

###Request

"发布_ml/anomaly_detectors/<job_id>/model_snapshots<snapshot_id>//_update"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

### 路径参数

`<job_id>`

     (Required, string) Identifier for the anomaly detection job. 
`<snapshot_id>`

     (Required, string) Identifier for the model snapshot. 

### 请求正文

创建模型快照后，可以更新以下属性：

`description`

     (Optional, string) A description of the model snapshot. 
`retain`

     (Optional, Boolean) If `true`, this snapshot will not be deleted during automatic cleanup of snapshots older than `model_snapshot_retention_days`. However, this snapshot will be deleted when the job is deleted. The default value is `false`. 

###Examples

    
    
    response = client.ml.update_model_snapshot(
      job_id: 'it_ops_new_logs',
      snapshot_id: 1_491_852_978,
      body: {
        description: 'Snapshot 1',
        retain: true
      }
    )
    puts response
    
    
    POST
    _ml/anomaly_detectors/it_ops_new_logs/model_snapshots/1491852978/_update
    {
      "description": "Snapshot 1",
      "retain": true
    }

更新快照时，您会收到以下结果：

    
    
    {
      "acknowledged": true,
      "model": {
        "job_id": "it_ops_new_logs",
        "timestamp": 1491852978000,
        "description": "Snapshot 1",
    ...
        "retain": true
      }
    }

[« Update anomaly detection jobs API](ml-update-job.md) [Upgrade model
snapshots API »](ml-upgrade-job-model-snapshot.md)



[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Delete anomaly detection jobs from calendar API](ml-delete-calendar-
job.md) [Delete expired data API »](ml-delete-expired-data.md)

## 删除模型快照接口

删除现有模型快照。

###Request

"删除_ml/anomaly_detectors/<job_id>/model_snapshots<snapshot_id>/"

###Prerequisites

需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

您无法删除活动模型快照。要删除该快照，请先恢复到其他快照。若要标识活动模型快照，请参阅获取作业 API 结果中的"model_snapshot_id"。

### 路径参数

`<job_id>`

     (Required, string) Identifier for the anomaly detection job. 
`<snapshot_id>`

     (Required, string) Identifier for the model snapshot. 

###Examples

    
    
    response = client.ml.delete_model_snapshot(
      job_id: 'farequote',
      snapshot_id: 1_491_948_163
    )
    puts response
    
    
    DELETE _ml/anomaly_detectors/farequote/model_snapshots/1491948163

删除快照后，您会收到以下结果：

    
    
    {
      "acknowledged": true
    }

[« Delete anomaly detection jobs from calendar API](ml-delete-calendar-
job.md) [Delete expired data API »](ml-delete-expired-data.md)

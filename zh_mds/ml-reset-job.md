

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Preview datafeeds API](ml-preview-datafeed.md) [Revert model snapshots
API »](ml-revert-snapshot.md)

## 重置异常检测作业API

重置现有的异常情况检测作业。

###Request

"发布_ml/anomaly_detectors<job_id>//_reset"

###Prerequisites

* 需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。  * 必须先关闭作业，然后才能重置作业。您可以在关闭作业时将"force"设置为"true"，以避免等待作业完成。请参阅关闭作业。

###Description

将删除所有模型状态和结果。作业已准备好重新开始，就像刚刚创建作业一样。

目前无法使用通配符或逗号分隔列表重置多个作业。

### 路径参数

`<job_id>`

     (Required, string) Identifier for the anomaly detection job. 

### 查询参数

`wait_for_completion`

     (Optional, Boolean) Specifies whether the request should return immediately or wait until the job reset completes. Defaults to `true`. 
`delete_user_annotations`

     (Optional, Boolean) Specifies whether annotations that have been added by the user should be deleted along with any auto-generated annotations when the job is reset. Defaults to `false`. 

###Examples

    
    
    response = client.ml.reset_job(
      job_id: 'total-requests'
    )
    puts response
    
    
    POST _ml/anomaly_detectors/total-requests/_reset

重置作业时，您会收到以下结果：

    
    
    {
      "acknowledged": true
    }

在下一个示例中，我们异步重置"总请求数"作业：

    
    
    response = client.ml.reset_job(
      job_id: 'total-requests',
      wait_for_completion: false
    )
    puts response
    
    
    POST _ml/anomaly_detectors/total-requests/_reset?wait_for_completion=false

当"wait_for_completion"设置为"false"时，响应包含作业重置任务的 id：

    
    
    {
      "task": "oTUltX4IQMOUUVeiohTt8A:39"
    }

如果要检查重置任务的状态，请通过引用任务 ID 来使用任务管理。

[« Preview datafeeds API](ml-preview-datafeed.md) [Revert model snapshots
API »](ml-revert-snapshot.md)

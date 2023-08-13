

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Rollup APIs](rollup-apis.md)

[« Create rollup jobs API](rollup-put-job.md) [Get rollup jobs API
»](rollup-get-job.md)

## 删除汇总作业API

删除现有汇总作业。

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

对于版本 8.5 及更高版本，我们建议对汇总进行缩减采样，以降低时序数据的存储成本。

###Request

"删除_rollup/作业/<job_id>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"或"manage_rollup"集群权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

必须先停止作业，然后才能将其删除。如果尝试删除已启动的作业，则会发生错误。同样，如果尝试删除不存在的作业，则会发生异常。

删除作业时，只会删除主动监视和汇总数据的进程。它不会删除任何以前汇总的数据。这是设计使然;用户可能希望汇总静态数据集。由于数据集是静态的，因此一旦完全汇总，就无需保留索引汇总作业(因为不会有新数据)。因此，可以删除作业，留下汇总的数据进行分析。

如果还希望删除汇总数据，并且汇总索引仅包含单个作业的数据，则只需删除整个汇总索引即可。如果汇总索引存储来自多个作业的数据，则必须发出以汇总索引中汇总作业的 ID 为目标的按删除查询。

    
    
    POST my_rollup_index/_delete_by_query
    {
      "query": {
        "term": {
          "_rollup.id": "the_rollup_job_id"
        }
      }
    }

### 路径参数

`<job_id>`

     (Required, string) Identifier for the job. 

### 响应码

"404"(缺少资源)

     This code indicates that there are no resources that match the request. It occurs if you try to delete a job that doesn't exist. 

###Example

如果我们有一个名为"sensor"的汇总作业，则可以通过以下方式删除它：

    
    
    response = client.rollup.delete_job(
      id: 'sensor'
    )
    puts response
    
    
    DELETE _rollup/job/sensor

这将返回响应：

    
    
    {
      "acknowledged": true
    }

[« Create rollup jobs API](rollup-put-job.md) [Get rollup jobs API
»](rollup-get-job.md)

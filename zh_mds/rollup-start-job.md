

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Rollup APIs](rollup-apis.md)

[« Rollup search](rollup-search.md) [Stop rollup jobs API »](rollup-stop-
job.md)

## 启动汇总作业API

启动现有的已停止汇总作业。

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

对于版本 8.5 及更高版本，我们建议对汇总进行缩减采样，以降低时序数据的存储成本。

###Request

"发布_rollup/工作/<job_id>/_start"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"或"manage_rollup"集群权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

如果尝试启动不存在的作业，则会发生异常。如果您尝试启动已启动的作业，则不会发生任何反应。

### 路径参数

`<job_id>`

     (Required, string) Identifier for the rollup job. 

### 响应码

"404"(缺少资源)

     This code indicates that there are no resources that match the request. It occurs if you try to start a job that doesn't exist. 

###Examples

如果我们已经创建了一个名为"sensor"的汇总作业，则可以从以下方面开始：

    
    
    response = client.rollup.start_job(
      id: 'sensor'
    )
    puts response
    
    
    POST _rollup/job/sensor/_start

这将返回响应：

    
    
    {
      "started": true
    }

[« Rollup search](rollup-search.md) [Stop rollup jobs API »](rollup-stop-
job.md)

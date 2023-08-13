

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Rollup APIs](rollup-apis.md)

[« Start rollup jobs API](rollup-start-job.md) [Script APIs »](script-
apis.md)

## 停止汇总作业API

停止现有的已启动汇总作业。

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

对于版本 8.5 及更高版本，我们建议对汇总进行缩减采样，以降低时序数据的存储成本。

###Request

"发布_rollup/工作/<job_id>/_stop"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"或"manage_rollup"集群权限才能使用此 API。有关详细信息，请参阅安全权限。

####Description

如果尝试停止不存在的作业，则会发生异常。如果尝试停止已停止的作业，则不会发生任何反应。

### 路径参数

`<job_id>`

     (Required, string) Identifier for the rollup job. 

### 查询参数

`timeout`

    

(可选，时间值)如果"wait_for_completion"为"true"，则 API 在等待作业停止时(最多)阻止指定的持续时间。如果超过"超时"时间，API 将引发超时异常。默认为"30s"。

即使抛出超时异常，停止请求仍在处理，并最终将作业移动到"已停止"。超时仅表示 API 调用本身在等待状态更改时超时。

`wait_for_completion`

     (Optional, Boolean) If set to `true`, causes the API to block until the indexer state completely stops. If set to `false`, the API returns immediately and the indexer is stopped asynchronously in the background. Defaults to `false`. 

### 响应码

"404"(缺少资源)

     This code indicates that there are no resources that match the request. It occurs if you try to stop a job that doesn't exist. 

###Examples

由于只能删除已停止的作业，因此在索引器完全停止之前阻止 API 会很有用。这是通过"wait_for_completion"查询参数和可选的"超时"完成的：

    
    
    response = client.rollup.stop_job(
      id: 'sensor',
      wait_for_completion: true,
      timeout: '10s'
    )
    puts response
    
    
    POST _rollup/job/sensor/_stop?wait_for_completion=true&timeout=10s

该参数阻止 API 调用返回，直到作业移动到"已停止"或经过指定的时间。如果指定的时间过去了，作业没有移动到"STOP"，则会引发超时异常。

[« Start rollup jobs API](rollup-start-job.md) [Script APIs »](script-
apis.md)



[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Roll up or
transform your data](data-rollup-transform.md) ›[Rolling up historical
data](xpack-rollup.md)

[« Rollup overview](rollup-overview.md) [Getting started with rollups
»](rollup-getting-started.md)

## 汇总 API 快速参考

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

对于版本 8.5 及更高版本，我们建议对汇总进行缩减采样，以降低时序数据的存储成本。

大多数汇总终结点具有以下基础：

    
    
    /_rollup/

####/工作/

* 放置 /_rollup/作业/：创建汇总作业 * 获取 /_rollup/作业：列出汇总作业 * 获取 /_rollup/作业/：获取汇总作业详细信息 * 发布 /_rollup/作业//_start：启动汇总作业 * 发布 /_rollup/作业//_stop：停止汇总作业 * 删除 /_rollup/作业<job_id><job_id><job_id><job_id>/<job_id>：删除汇总作业

####/数据/

* 获取 /_rollup/data//_rollup_caps：获取汇总功能 * 获取 //<index_pattern><index_name>_rollup/data/：获取汇总索引功能

####/<index_name>/

* GET /<index_name>/_rollup_search：搜索汇总数据

[« Rollup overview](rollup-overview.md) [Getting started with rollups
»](rollup-getting-started.md)

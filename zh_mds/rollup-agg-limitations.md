

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Roll up or
transform your data](data-rollup-transform.md) ›[Rolling up historical
data](xpack-rollup.md)

[« Understanding groups](rollup-understanding-groups.md) [Rollup search
limitations »](rollup-search-limitations.md)

## 汇总聚合限制

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

对于版本 8.5 及更高版本，我们建议对汇总进行缩减采样，以降低时序数据的存储成本。

字段的汇总/聚合方式存在一些限制。本页重点介绍主要限制，以便您了解这些限制。

#### 有限的聚合组件

汇总功能允许使用以下聚合对字段进行分组：

* 日期直方图聚合 * 直方图聚合 * 术语聚合

并且允许为数值字段指定以下指标：

* 最小聚合 * 最大聚合 * 总和聚合 * 平均聚合 * 值计数聚合

[« Understanding groups](rollup-understanding-groups.md) [Rollup search
limitations »](rollup-search-limitations.md)

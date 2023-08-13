

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Split index API](indices-split-index.md) [Update index settings API
»](indices-update-settings.md)

## 解冻索引API

### 7.14 中已弃用

在 8.0 中，我们删除了冻结索引的功能。在以前的版本中，冻结索引可减少其内存开销。但是，由于最近堆内存使用率的改进，冻结索引不再有用。您可以使用此 API 解冻在 7.x 中冻结的索引。冻结索引与冻结数据层无关。

解冻索引。

###Request

"发布/<index>/_unfreeze"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标索引或索引别名具有"管理"索引权限。

###Description

当冻结的索引解冻时，索引将经历正常的恢复过程并再次变为可写状态。

### 路径参数

`<index>`

     (Required, string) Identifier for the index. 

###Examples

以下示例解冻索引：

    
    
    response = client.indices.unfreeze(
      index: 'my-index-000001'
    )
    puts response
    
    
    POST /my-index-000001/_unfreeze

[« Split index API](indices-split-index.md) [Update index settings API
»](indices-update-settings.md)

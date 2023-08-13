

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Delete index template API](indices-delete-template.md) [Exists API
»](indices-exists.md)

## 删除索引模板接口

本文档是关于遗留索引模板的，这些模板已被弃用，将被 Elasticsearch 7.8 中引入的可组合模板所取代。有关可组合模板的信息，请参阅索引模板。

删除旧版索引模板。

    
    
    response = client.indices.delete_template(
      name: 'my-legacy-index-template'
    )
    puts response
    
    
    DELETE /_template/my-legacy-index-template

###Request

"删除/_template/<legacy-index-template>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"manage_index_templates"或"管理"集群权限才能使用此 API。

### 路径参数

`<legacy-index-template>`

     (Required, string) The name of the legacy index template to delete. Wildcard (`*`) expressions are supported. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

[« Delete index template API](indices-delete-template.md) [Exists API
»](indices-exists.md)

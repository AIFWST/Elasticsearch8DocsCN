

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Get index template API](indices-get-template-v1.md) [Import dangling
index API »](dangling-index-import.md)

## 获取映射接口

检索一个或多个索引的映射定义。对于数据流，API 检索流的支持索引的映射。

    
    
    response = client.indices.get_mapping(
      index: 'my-index-000001'
    )
    puts response
    
    
    res, err := es.Indices.GetMapping(es.Indices.GetMapping.WithIndex("my-index-000001"))
    fmt.Println(res, err)
    
    
    GET /my-index-000001/_mapping

###Request

"获取/_mapping"

"获取/<target>/_mapping"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"view_index_metadata"或"管理"索引权限。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases used to limit the request. Supports wildcards (`*`). To target all data streams and indices, omit this parameter or use `*` or `_all`. 

### 查询参数

`allow_no_indices`

    

(可选，布尔值)如果为"false"，则当任何通配符表达式、索引别名或"_all"值仅针对缺少或关闭的索引时，请求将返回错误。即使请求以其他打开的索引为目标，此行为也适用。例如，如果索引以"foo"开头但没有索引以"bar"开头，则以"foo*，bar*"为目标的请求将返回错误。

默认为"真"。

`expand_wildcards`

    

(可选，字符串)通配符模式可以匹配的索引类型。如果请求可以以数据流为目标，则此参数确定通配符表达式是否与隐藏的数据流匹配。支持逗号分隔的值，例如"打开，隐藏"。有效值为：

`all`

     Match any data stream or index, including [hidden](api-conventions.html#multi-hidden "Hidden data streams and indices") ones. 
`open`

     Match open, non-hidden indices. Also matches any non-hidden data stream. 
`closed`

     Match closed, non-hidden indices. Also matches any non-hidden data stream. Data streams cannot be closed. 
`hidden`

     Match hidden data streams and hidden indices. Must be combined with `open`, `closed`, or both. 
`none`

     Wildcard patterns are not accepted. 

默认为"打开"。

`ignore_unavailable`

     (Optional, Boolean) If `false`, the request returns an error if it targets a missing or closed index. Defaults to `false`. 
`local`

     (Optional, Boolean) If `true`, the request retrieves information from the local node only. Defaults to `false`, which means information is retrieved from the master node. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

#### 多个数据流和索引

获取映射 API 可用于通过单个调用获取多个数据流或索引。API 的一般用法遵循以下语法："host：port/<target>/_mapping"，其中"<target>"可以接受逗号分隔的名称列表。要获取集群中所有数据流和索引的映射，请使用"_all"或"*"表示<target>""或省略"<target>"参数。以下是一些示例：

    
    
    response = client.indices.get_mapping(
      index: 'my-index-000001,my-index-000002'
    )
    puts response
    
    
    GET /my-index-000001,my-index-000002/_mapping

如果要获取集群中所有索引的映射，以下示例是等效的：

    
    
    $params = [
        'index' => '*',
    ];
    $response = $client->indices()->getMapping($params);
    $params = [
        'index' => '_all',
    ];
    $response = $client->indices()->getMapping($params);
    $response = $client->indices()->getMapping();
    
    
    response = client.indices.get_mapping(
      index: '*'
    )
    puts response
    
    response = client.indices.get_mapping(
      index: '_all'
    )
    puts response
    
    response = client.indices.get_mapping
    puts response
    
    
    {
    	res, err := es.Indices.GetMapping(es.Indices.GetMapping.WithIndex("*"))
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Indices.GetMapping(es.Indices.GetMapping.WithIndex("_all"))
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Indices.GetMapping()
    	fmt.Println(res, err)
    }
    
    
    GET /*/_mapping
    
    GET /_all/_mapping
    
    GET /_mapping

[« Get index template API](indices-get-template-v1.md) [Import dangling
index API »](dangling-index-import.md)

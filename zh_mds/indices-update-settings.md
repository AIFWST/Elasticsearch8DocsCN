

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Unfreeze index API](unfreeze-index-api.md) [Update mapping API
»](indices-put-mapping.md)

## 更新索引设置接口

实时更改动态索引设置。

对于数据流，默认情况下，索引设置更改将应用于所有后备索引。

    
    
    response = client.indices.put_settings(
      index: 'my-index-000001',
      body: {
        index: {
          number_of_replicas: 2
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001/_settings
    {
      "index" : {
        "number_of_replicas" : 2
      }
    }

###Request

"放 /<target>/_settings"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"管理"索引权限。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases used to limit the request. Supports wildcards (`*`). To target all data streams and indices, omit this parameter or use `*` or `_all`. 

### 查询参数

`allow_no_indices`

    

(可选，布尔值)如果为"false"，则当任何通配符表达式、索引别名或"_all"值仅针对缺少或关闭的索引时，请求将返回错误。即使请求以其他打开的索引为目标，此行为也适用。例如，如果索引以"foo"开头但没有索引以"bar"开头，则以"foo*，bar*"为目标的请求将返回错误。

默认为"假"。

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

`flat_settings`

     (Optional, Boolean) If `true`, returns settings in flat format. Defaults to `false`. 
`ignore_unavailable`

     (Optional, Boolean) If `false`, the request returns an error if it targets a missing or closed index. Defaults to `false`. 
`preserve_existing`

     (Optional, Boolean) If `true`, existing index settings remain unchanged. Defaults to `false`. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 请求正文

`settings`

     (Optional, [index setting object](index-modules.html#index-modules-settings "Index Settings")) Configuration options for the index. See [Index Settings](index-modules.html#index-modules-settings "Index Settings"). 

###Examples

#### 重置索引设置

要将设置恢复为默认值，请使用"null"。例如：

    
    
    response = client.indices.put_settings(
      index: 'my-index-000001',
      body: {
        index: {
          refresh_interval: nil
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001/_settings
    {
      "index" : {
        "refresh_interval" : null
      }
    }

可以在 Index 模块中找到可以在 liveindex 上动态更新的每个索引设置列表。要保持现有设置不被更新，可以将"preserve_existing"请求参数设置为"true"。

#### 批量索引用法

例如，更新设置 API 可用于动态更改索引，使其从批量索引的性能更高，然后将其移动到更实时的索引状态。在开始批量索引之前，请使用：

    
    
    response = client.indices.put_settings(
      index: 'my-index-000001',
      body: {
        index: {
          refresh_interval: '-1'
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001/_settings
    {
      "index" : {
        "refresh_interval" : "-1"
      }
    }

(另一个优化选项是在没有任何副本的情况下启动索引，然后再添加它们，但这实际上取决于用例)。

然后，一旦批量索引完成，就可以更新设置(例如，返回到默认值)：

    
    
    response = client.indices.put_settings(
      index: 'my-index-000001',
      body: {
        index: {
          refresh_interval: '1s'
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001/_settings
    {
      "index" : {
        "refresh_interval" : "1s"
      }
    }

并且，应调用强制合并：

    
    
    response = client.indices.forcemerge(
      index: 'my-index-000001',
      max_num_segments: 5
    )
    puts response
    
    
    POST /my-index-000001/_forcemerge?max_num_segments=5

#### 更新索引分析

您只能在已关闭的索引上定义新的分析器。

若要添加分析器，必须关闭索引，定义分析器，然后重新打开索引。

您无法关闭数据流的写入索引。

要更新数据流的写入索引和未来支持索引的分析器，请在流使用的索引模板中更新分析器。然后滚动数据流，将新分析器应用于流的写入索引和将来的支持索引。这会影响搜索和滚动更新后添加到流的任何新数据。但是，它不会影响数据流的支持索引或其现有数据。

若要更改现有后备索引的分析器，必须创建一个 newdata 流并将数据重新索引到其中。请参阅使用重新索引更改映射或设置。

例如，以下命令将"内容"分析器添加到"my-index-000001"索引：

    
    
    response = client.indices.close(
      index: 'my-index-000001'
    )
    puts response
    
    response = client.indices.put_settings(
      index: 'my-index-000001',
      body: {
        analysis: {
          analyzer: {
            content: {
              type: 'custom',
              tokenizer: 'whitespace'
            }
          }
        }
      }
    )
    puts response
    
    response = client.indices.open(
      index: 'my-index-000001'
    )
    puts response
    
    
    POST /my-index-000001/_close
    
    PUT /my-index-000001/_settings
    {
      "analysis" : {
        "analyzer":{
          "content":{
            "type":"custom",
            "tokenizer":"whitespace"
          }
        }
      }
    }
    
    POST /my-index-000001/_open

[« Unfreeze index API](unfreeze-index-api.md) [Update mapping API
»](indices-put-mapping.md)



[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search APIs](search.md)

[« Validate API](search-validate.md) [Explain API »](search-explain.md)

## 术语枚举API

术语枚举 API 可用于发现索引中与部分字符串匹配的术语。支持的字段类型包括"关键字"、"constant_keyword"、"平展"、"版本"和"IP"。这用于自动完成：

    
    
    response = client.terms_enum(
      index: 'stackoverflow',
      body: {
        field: 'tags',
        string: 'kiba'
      }
    )
    puts response
    
    
    POST stackoverflow/_terms_enum
    {
        "field" : "tags",
        "string" : "kiba"
    }

API 返回以下响应：

    
    
    {
      "_shards": {
        "total": 1,
        "successful": 1,
        "failed": 0
      },
      "terms": [
        "kibana"
      ],
      "complete" : true
    }

如果"complete"标志为"false"，则返回的"terms"集可能不完整，应被视为近似值。这可能是由于几个原因造成的，例如请求超时或节点错误。

术语枚举 API 可能会从已删除的文档中返回术语。已删除的文档最初仅标记为已删除。直到他们的片段出现，文档才真正被删除。在此之前，术语枚举 API 将从这些文档中返回术语。

###Request

"获取/<target>/_terms_enum"

###Description

terms_enum API 可用于发现索引中以提供的字符串开头的术语。它专为自动完成方案中使用的低延迟查找而设计。

### 路径参数

`<target>`

     (Required, string) Comma-separated list of data streams, indices, and aliases to search. Supports wildcards (`*`). To search all data streams or indices, omit this parameter or use `*` or `_all`. 

### 请求正文

`field`

     (Mandatory, string) Which field to match 

`string`

     (Optional, string) The string to match at the start of indexed terms. If not provided, all terms in the field are considered. 

`size`

     (Optional, integer) How many matching terms to return. Defaults to 10 

`timeout`

     (Optional, [time value](api-conventions.html#time-units "Time units")) The maximum length of time to spend collecting results. Defaults to "1s" (one second). If the timeout is exceeded the `complete` flag set to false in the response and the results may be partial or empty. 

`case_insensitive`

     (Optional, boolean) When true the provided search string is matched against index terms without case sensitivity. Defaults to false. 

`index_filter`

     (Optional, [query object](query-dsl.html "Query DSL") Allows to filter an index shard if the provided query rewrites to `match_none`. 

`search_after`

     (Optional, string) The string after which terms in the index should be returned. Allows for a form of pagination if the last result from one request is passed as the `search_after` parameter for a subsequent request. 

[« Validate API](search-validate.md) [Explain API »](search-explain.md)

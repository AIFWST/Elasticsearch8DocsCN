

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search APIs](search.md)

[« Profile API](search-profile.md) [Ranking evaluation API »](search-rank-
eval.md)

## 字段功能接口

允许您在多个索引中检索字段的功能。对于数据流，API 在流的支持索引中返回字段功能。

    
    
    response = client.field_caps(
      fields: 'rating'
    )
    puts response
    
    
    GET /_field_caps?fields=rating

###Request

'GET /_field_caps？fields=<fields>'

'POST /_field_caps？fields=<fields>'

'GET /<target>/_field_caps？fields=<fields>'

'POST /<target>/_field_caps？fields=<fields>'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"view_index_metadata"、"读取"或"管理"索引权限。

###Description

字段功能 API 返回有关多个索引中字段的功能的信息。

字段功能 API 像任何其他字段一样返回运行时字段。例如，类型为"关键字"的运行时字段将作为属于"关键字"系列的任何其他字段返回。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases used to limit the request. Supports wildcards (`*`). To target all data streams and indices, omit this parameter or use `*` or `_all`. 

### 查询参数

`fields`

     (Required, string) Comma-separated list of fields to retrieve capabilities for. Wildcard (`*`) expressions are supported. 
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
`include_unmapped`

     (Optional, Boolean) If `true`, unmapped fields that are mapped in one index but not in another are included in the response. Fields that don't have any mapping are never included. Defaults to `false`. 
`filters`

    

(可选，字符串)要应用于响应的筛选器的逗号分隔列表。

"过滤器"的有效值

`+metadata`

     Only include metadata fields 
`-metadata`

     Exclude metadata fields 
`-parent`

     Exclude parent fields 
`-nested`

     Exclude nested fields 
`-multifield`

     Exclude multifields 

`types`

     (Optional, string) Comma-separated list of field types to include. Any fields that do not match one of these types will be excluded from the results. Defaults to empty, meaning that all field types are returned. See [here](search-field-caps.html#field-caps-field-types) for more information about field types in field capabilities requests and responses. 

### 请求正文

`index_filter`

     (Optional, [query object](query-dsl.html "Query DSL") Allows to filter indices if the provided query rewrites to `match_none` on every shard. 
`runtime_mappings`

     (Optional, object) Defines ad-hoc [runtime fields](runtime-search-request.html "Define runtime fields in a search request") in the request similar to the way it is done in [search requests](search-search.html#search-api-body-runtime). These fields exist only as part of the query and take precedence over fields defined with the same name in the index mappings. 

### 响应正文

响应中使用的类型描述字段类型的_系列_。通常，atype 族与映射中声明的字段类型相同，但为了简单起见，使用类型族来描述某些行为相同的字段类型。例如，"关键字"、"constant_keyword"和"通配符"字段类型都被描述为"关键字"类型系列。

`metadata_field`

     Whether this field is registered as a [metadata field](mapping-fields.html "Metadata fields"). 
`searchable`

     Whether this field is indexed for search on all indices. 
`aggregatable`

     Whether this field can be aggregated on all indices. 
`time_series_dimension`

     Whether this field is used as a time series dimension on all indices. For non-time-series indices this field is not present. 
`time_series_metric`

     Contains the metric type if the field is used as a time series metric on all indices, absent if the field is not used as a metric. For non-time-series indices this field is not included. 
`indices`

     The list of indices where this field has the same type family, or null if all indices have the same type family for the field. 
`non_searchable_indices`

     The list of indices where this field is not searchable, or null if all indices have the same definition for the field. 
`non_aggregatable_indices`

     The list of indices where this field is not aggregatable, or null if all indices have the same definition for the field. 
`non_dimension_indices`

     [preview]  This functionality is in technical preview and may be changed or removed in a future release. Elastic will apply best effort to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.  If this list is present in the response, some indices have the field marked as a dimension and other indices, the ones in this list, do not. 
`metric_conflicts_indices`

     [preview]  This functionality is in technical preview and may be changed or removed in a future release. Elastic will apply best effort to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.  The list of indices where this field is present, if these indices don't have the same `time_series_metric` value for this field. 
`meta`

     Merged metadata across all indices as a map of string keys to arrays of values. A value length of 1 indicates that all indices had the same value for this key, while a length of 2 or more indicates that not all indices had the same value for this key. 

###Examples

可以将请求限制为特定的数据流和索引：

    
    
    response = client.field_caps(
      index: 'my-index-000001',
      fields: 'rating'
    )
    puts response
    
    
    GET my-index-000001/_field_caps?fields=rating

下一个示例 API 调用请求有关"评级"和"标题"字段的信息：

    
    
    response = client.field_caps(
      fields: 'rating,title'
    )
    puts response
    
    
    GET _field_caps?fields=rating,title

API 返回以下响应：

    
    
    {
      "indices": [ "index1", "index2", "index3", "index4", "index5" ],
      "fields": {
        "rating": {                                   __"long": {
            "metadata_field": false,
            "searchable": true,
            "aggregatable": false,
            "indices": [ "index1", "index2" ],
            "non_aggregatable_indices": [ "index1" ] __},
          "keyword": {
            "metadata_field": false,
            "searchable": false,
            "aggregatable": true,
            "indices": [ "index3", "index4" ],
            "non_searchable_indices": [ "index4" ] __}
        },
        "title": { __"text": {
            "metadata_field": false,
            "searchable": true,
            "aggregatable": false
          }
        }
      }
    }

__

|

字段"rating"定义为"index1"和"index2"中的长整型，以及"index3"和"index4"中的"关键字"。   ---|---    __

|

字段"评级"不可在"index1"中聚合。   __

|

字段"评级"在"索引4"中不可搜索。   __

|

字段"title"在所有索引中都定义为"文本"。   默认情况下，将忽略未映射的字段。您可以通过在请求中添加名为"include_unmapped"的参数将它们包含在响应中：

    
    
    response = client.field_caps(
      fields: 'rating,title',
      include_unmapped: true
    )
    puts response
    
    
    GET _field_caps?fields=rating,title&include_unmapped

在这种情况下，响应将包含某些索引中存在的每个字段的条目，但不是全部：

    
    
    {
      "indices": [ "index1", "index2", "index3" ],
      "fields": {
        "rating": {
          "long": {
            "metadata_field": false,
            "searchable": true,
            "aggregatable": false,
            "indices": [ "index1", "index2" ],
            "non_aggregatable_indices": [ "index1" ]
          },
          "keyword": {
            "metadata_field": false,
            "searchable": false,
            "aggregatable": true,
            "indices": [ "index3", "index4" ],
            "non_searchable_indices": [ "index4" ]
          },
          "unmapped": {                               __"metadata_field": false,
            "indices": [ "index5" ],
            "searchable": false,
            "aggregatable": false
          }
        },
        "title": {
          "text": {
            "metadata_field": false,
            "indices": [ "index1", "index2", "index3", "index4" ],
            "searchable": true,
            "aggregatable": false
          },
          "unmapped": { __"metadata_field": false,
            "indices": [ "index5" ],
            "searchable": false,
            "aggregatable": false
          }
        }
      }
    }

__

|

"index5"中的"评级"字段未映射。   ---|---    __

|

"index5"中的"标题"字段未映射。   也可以使用查询过滤索引：

    
    
    response = client.field_caps(
      index: 'my-index-*',
      fields: 'rating',
      body: {
        index_filter: {
          range: {
            "@timestamp": {
              gte: '2018'
            }
          }
        }
      }
    )
    puts response
    
    
    POST my-index-*/_field_caps?fields=rating
    {
      "index_filter": {
        "range": {
          "@timestamp": {
            "gte": "2018"
          }
        }
      }
    }

在这种情况下，将在每个分片上将提供的过滤器重写为"match_none"的索引将从响应中过滤掉。

过滤是在尽力而为的基础上完成的，它使用索引统计信息和映射将查询重写为"match_none"，而不是完全执行请求。例如，如果分片中的所有文档(包括已删除的文档)都在提供的范围之外，则对"日期"字段的"范围"查询可以重写为"match_none"。但是，并非所有查询都可以重写为"match_none"，因此即使提供的筛选器与文档不匹配，此 API 也可能返回索引。

[« Profile API](search-profile.md) [Ranking evaluation API »](search-rank-
eval.md)

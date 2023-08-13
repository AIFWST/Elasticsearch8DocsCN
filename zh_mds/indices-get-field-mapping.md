

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Index APIs](indices.md)

[« Get component template API](getting-component-templates.md) [Get index
API »](indices-get-index.md)

## 获取字段映射接口

检索一个或多个字段的映射定义。对于数据流，API 检索流的支持索引的字段映射。

如果不需要完整的映射或索引映射包含大量字段，则此 API 非常有用。

    
    
    response = client.indices.get_field_mapping(
      index: 'my-index-000001',
      fields: 'user'
    )
    puts response
    
    
    GET /my-index-000001/_mapping/field/user

###Request

'获取/_mapping/字段/<field>'

'GET //<target>_mapping/field/<field>'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或别名具有"view_index_metadata"或"管理"索引权限。

### 路径参数

`<target>`

     (Optional, string) Comma-separated list of data streams, indices, and aliases used to limit the request. Supports wildcards (`*`). To target all data streams and indices, omit this parameter or use `*` or `_all`. 
`<field>`

     (Optional, string) Comma-separated list or wildcard expression of fields used to limit returned information. 

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

`ignore_unavailable`

     (Optional, Boolean) If `false`, the request returns an error if it targets a missing or closed index. Defaults to `false`. 
`include_defaults`

     (Optional, Boolean) If `true`, the response includes default mapping values. Defaults to `false`. 

###Examples

#### 索引设置示例

您可以在创建新索引时提供字段映射。以下创建索引 API 请求创建具有多个字段映射的"发布"索引。

    
    
    response = client.indices.create(
      index: 'publications',
      body: {
        mappings: {
          properties: {
            id: {
              type: 'text'
            },
            title: {
              type: 'text'
            },
            abstract: {
              type: 'text'
            },
            author: {
              properties: {
                id: {
                  type: 'text'
                },
                name: {
                  type: 'text'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /publications
    {
      "mappings": {
        "properties": {
          "id": { "type": "text" },
          "title": { "type": "text" },
          "abstract": { "type": "text" },
          "author": {
            "properties": {
              "id": { "type": "text" },
              "name": { "type": "text" }
            }
          }
        }
      }
    }

以下内容仅返回字段"title"的映射：

    
    
    response = client.indices.get_field_mapping(
      index: 'publications',
      fields: 'title'
    )
    puts response
    
    
    GET publications/_mapping/field/title

API 返回以下响应：

    
    
    {
       "publications": {
          "mappings": {
              "title": {
                 "full_name": "title",
                 "mapping": {
                    "title": {
                       "type": "text"
                    }
                 }
              }
           }
       }
    }

#### 指定字段

获取映射 API 允许您指定以逗号分隔的字段列表。

例如，要选择"作者"字段的"id"，您必须使用其全名"author.id"。

    
    
    response = client.indices.get_field_mapping(
      index: 'publications',
      fields: 'author.id,abstract,name'
    )
    puts response
    
    
    GET publications/_mapping/field/author.id,abstract,name

returns:

    
    
    {
       "publications": {
          "mappings": {
            "author.id": {
               "full_name": "author.id",
               "mapping": {
                  "id": {
                     "type": "text"
                  }
               }
            },
            "abstract": {
               "full_name": "abstract",
               "mapping": {
                  "abstract": {
                     "type": "text"
                  }
               }
            }
         }
       }
    }

获取字段映射 API 还支持通配符表示法。

    
    
    response = client.indices.get_field_mapping(
      index: 'publications',
      fields: 'a*'
    )
    puts response
    
    
    GET publications/_mapping/field/a*

returns:

    
    
    {
       "publications": {
          "mappings": {
             "author.name": {
                "full_name": "author.name",
                "mapping": {
                   "name": {
                     "type": "text"
                   }
                }
             },
             "abstract": {
                "full_name": "abstract",
                "mapping": {
                   "abstract": {
                      "type": "text"
                   }
                }
             },
             "author.id": {
                "full_name": "author.id",
                "mapping": {
                   "id": {
                      "type": "text"
                   }
                }
             }
          }
       }
    }

#### 多个目标和字段

获取字段映射 API 可用于通过单个请求从多个数据流或索引获取多个字段的映射。

"<target>"和<field>""请求路径参数都支持逗号分隔列表和通配符表达式。

您可以省略 '' <target>参数或使用值 '*' 或 '_all' 来定位集群中的所有数据流和索引。

同样，您可以省略 '' <field>参数或使用值 '*' 来检索目标数据流或索引中所有字段的映射。但是，<field>""参数不支持"_all"值。

例如，以下请求检索名为"my-index-000001"或"my-index-000002"的任何数据流或索引中"消息"字段的映射。

    
    
    response = client.indices.get_field_mapping(
      index: 'my-index-000001,my-index-000002',
      fields: 'message'
    )
    puts response
    
    
    GET /my-index-000001,my-index-000002/_mapping/field/message

以下请求检索集群中任何数据流或索引中的"消息"和"user.id"字段的映射。

    
    
    response = client.indices.get_field_mapping(
      index: '_all',
      fields: 'message'
    )
    puts response
    
    
    GET /_all/_mapping/field/message

以下请求检索群集中任何数据流或索引中具有"id"属性的字段的映射。

    
    
    response = client.indices.get_field_mapping(
      index: '_all',
      fields: '*.id'
    )
    puts response
    
    
    GET /_all/_mapping/field/*.id

[« Get component template API](getting-component-templates.md) [Get index
API »](indices-get-index.md)

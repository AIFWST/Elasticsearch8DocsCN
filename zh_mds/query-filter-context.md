

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md)

[« Query DSL](query-dsl.md) [Compound queries »](compound-queries.md)

## 查询和筛选上下文

### 相关性分数

默认情况下，Elasticsearch 按相关性分数对匹配的搜索结果进行排序，该分数衡量每个文档与查询的匹配程度。

相关性分数是一个正浮点数，在搜索 API 的"_score"元数据字段中返回。"_score"越高，文档越相关。虽然每种查询类型可以以不同的方式计算相关性分数，但分数计算还取决于查询子句是在 **query** 还是 **filter** 上下文中运行。

### query context

query context中，查询子句回答问题"此文档与此查询子句有多匹配？“除了确定文档是否匹配外，查询子句还会计算"_score"元数据字段中的相关性分数。

每当将查询子句传递给"查询"参数(例如搜索 API 中的"查询"参数)时，查询上下文就会生效。

### filter context

在filter context中，查询子句回答问题"此文档是否匹配此查询子句？"答案是简单的"是"或"否"，不计算分数。过滤器上下文主要用于过滤结构化数据，例如

* 这个"time"是否落在 2015 到 2016 的范围内？"状态"字段是否设置为"已发布"？

常用的过滤器将由 Elasticsearch 自动缓存，以加快性能。

每当将查询子句传递给"filter"参数(例如"bool"查询中的"filter"或"must_not"参数、"constant_score"查询中的"filter"参数或"filter"聚合)时，filter context就会生效。

### 查询和筛选器上下文示例

下面是在"_search"API 的查询和筛选器上下文中使用的查询子句的示例。此查询将匹配满足以下所有条件的文档：

* "title"字段包含"Search"。  * "content"字段包含"Elasticsearch"一词。  
* "status"字段包含确切的"published"一词。  
* "publish_date"字段包含 2015 年 1 月 1 日起的日期。
 
```python
resp = client.search(
    body={
        "query": {
            "bool": {
                "must": [
                    {"match": {"title": "Search"}},
                    {"match": {"content": "Elasticsearch"}},
                ],
                "filter": [
                    {"term": {"status": "published"}},
                    {"range": {"publish_date": {"gte": "2015-01-01"}}},
                ],
            }
        }
    },
)
print(resp)
```
    
puts response 
```
GET /_search
{
  "query": { 
    "bool": { 
        "must": [
        { "match": { "title":   "Search" }},
        { "match": { "content": "Elasticsearch" }}
      ],
      "filter": [ 
        { "term":  { "status": "published" }},
        { "range": { "publish_date": { "gte": "2015-01-01" }}}
      ]
    }
  }
}
```

"query"参数指示查询上下文。 

"bool"和两个"match"子句用于查询上下文，这意味着它们用于对每个文档的匹配程度进行评分。

"filter"参数指示过滤器上下文。它的"term"和"range"子句用于过滤器上下文。它们将过滤掉不匹配的文档，但不会影响匹配文档的分数。   为查询上下文中的查询计算的分数表示为单精度浮点数;它们只有 24 位用于 Significand 的精度。超过有效数精度的分数计算将转换为精度损失的浮点数。

在查询上下文中使用查询子句来查找应影响匹配文档分数的条件(即文档的匹配程度)，并在筛选器上下文中使用所有其他查询子句。

[« Query DSL](query-dsl.md) [Compound queries »](compound-queries.md)

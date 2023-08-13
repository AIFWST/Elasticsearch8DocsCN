

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Rank features field type](rank-features.md) [Shape field type
»](shape.md)

## 键入时搜索字段类型

"search_as_you_type"字段类型是一个类似文本的字段，经过优化，可为提供即类型完成用例的查询提供开箱即用的支持。它创建一系列子字段，分析这些子字段以索引术语，这些术语可以通过部分匹配整个索引文本值的查询进行有效匹配。支持前缀补全(即匹配术语从输入开头开始)和中缀补全(即匹配输入内任何位置的术语)。

将此类型的字段添加到映射时

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            my_field: {
              type: 'search_as_you_type'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "my_field": {
            "type": "search_as_you_type"
          }
        }
      }
    }

这将创建以下字段

`my_field`

|

按照映射中的配置进行分析。如果未配置分析器，则使用索引的默认分析器---|--- 'my_field._2gram'

|

用带状疱疹尺寸为 2 'my_field._3gram' 的带状疱疹令牌过滤器包裹"my_field"分析仪

|

使用带状疱疹大小为 3 的带状疱疹令牌过滤器包装"my_field"的分析器my_field._index_前缀

|

使用边缘 ngram 标记筛选器包装"my_field._3gram"的分析器 可以使用"max_shingle_size"映射参数配置子字段中带状疱疹的大小。默认值为 3，此参数的有效值为整数值 2 - 4(含)。将为从 2 到"max_shingle_size"的每个瓦片尺寸创建带状疱疹子字段。在构造自己的分析器时，"my_field._index_prefix"子字段将始终使用带有"max_shingle_size"的带状疱疹子字段中的分析器。

增加"max_shingle_size"将改善具有更多连续字词的查询的匹配，但代价是索引大小更大。默认值"max_shingle_size"通常就足够了。

当索引文档具有根字段"my_field"的值时，相同的输入文本将自动索引到这些字段中，并具有不同的分析链。

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      refresh: true,
      body: {
        my_field: 'quick brown fox jump lazy dog'
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/1?refresh
    {
      "my_field": "quick brown fox jump lazy dog"
    }

为按需搜索用例提供最有效的查询方式通常是针对根"search_as_you_type"字段及其带状疱疹子字段的"multi_match"查询，类型为"bool_prefix"。这可以按任何顺序匹配查询词，但如果文档在 shinglesub 字段中按顺序包含这些词，则会对文档进行更高的评分。

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          multi_match: {
            query: 'brown f',
            type: 'bool_prefix',
            fields: [
              'my_field',
              'my_field._2gram',
              'my_field._3gram'
            ]
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "query": {
        "multi_match": {
          "query": "brown f",
          "type": "bool_prefix",
          "fields": [
            "my_field",
            "my_field._2gram",
            "my_field._3gram"
          ]
        }
      }
    }
    
    
    {
      "took" : 44,
      "timed_out" : false,
      "_shards" : {
        "total" : 1,
        "successful" : 1,
        "skipped" : 0,
        "failed" : 0
      },
      "hits" : {
        "total" : {
          "value" : 1,
          "relation" : "eq"
        },
        "max_score" : 0.8630463,
        "hits" : [
          {
            "_index" : "my-index-000001",
            "_id" : "1",
            "_score" : 0.8630463,
            "_source" : {
              "my_field" : "quick brown fox jump lazy dog"
            }
          }
        ]
      }
    }

要按顺序搜索与查询词严格匹配的文档，或使用短语查询的其他属性进行搜索，请在根字段上使用"match_phrase_prefix"查询。如果最后一个术语应完全匹配，而不是作为前缀，也可以使用"match_phrase"查询。使用短语查询的效率可能低于使用"match_bool_prefix"查询。

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          match_phrase_prefix: {
            my_field: 'brown f'
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "query": {
        "match_phrase_prefix": {
          "my_field": "brown f"
        }
      }
    }

### 特定于"search_as_you_type"字段的参数

以下参数在"search_as_you_type"字段的映射中被接受，并且特定于此字段类型

`max_shingle_size`

    

(可选，整数)创建的最大瓦片尺寸。有效值为"2"(含)到"4"(含)。默认为"3"。

将为"2"和此值之间的每个整数创建一个子字段。例如，值"3"会创建两个子字段："my_field._2gram"和"my_field._3gram"

更多的子字段可以启用更具体的查询，但会增加索引大小。

### 作为文本字段的字段类型的参数

由于以下参数的性质是类似文本的字段，因此在"search_as_you_type"字段的映射中被接受，并且在配置"text"数据类型的字段时，其行为类似于它们的行为。除非另有说明，否则这些选项以相同的方式配置根字段子字段。

"分析器"

     The [analyzer](analysis.html "Text analysis") which should be used for `text` fields, both at index-time and at search-time (unless overridden by the [`search_analyzer`](search-analyzer.html "search_analyzer")). Defaults to the default index analyzer, or the [`standard` analyzer](analysis-standard-analyzer.html "Standard analyzer"). 
[`index`](mapping-index.html "index")

     Should the field be searchable? Accepts `true` (default) or `false`. 
[`index_options`](index-options.html "index_options")

     What information should be stored in the index, for search and highlighting purposes. Defaults to `positions`. 
[`norms`](norms.html "norms")

     Whether field-length should be taken into account when scoring queries. Accepts `true` or `false`. This option configures the root field and shingle subfields, where its default is `true`. It does not configure the prefix subfield, where it is `false`. 
[`store`](mapping-store.html "store")

     Whether the field value should be stored and retrievable separately from the [`_source`](mapping-source-field.html "_source field") field. Accepts `true` or `false` (default). This option only configures the root field, and does not configure any subfields. 
[`search_analyzer`](search-analyzer.html "search_analyzer")

     The [`analyzer`](analyzer.html "analyzer") that should be used at search time on [`text`](text.html "Text type family") fields. Defaults to the `analyzer` setting. 
[`search_quote_analyzer`](analyzer.html#search-quote-analyzer
"search_quote_analyzer")

     The [`analyzer`](analyzer.html "analyzer") that should be used at search time when a phrase is encountered. Defaults to the `search_analyzer` setting. 
[`similarity`](similarity.html "similarity")

     Which scoring algorithm or _similarity_ should be used. Defaults to `BM25`. 
[`term_vector`](term-vector.html "term_vector")

     Whether term vectors should be stored for the field. Defaults to `no`. This option configures the root field and shingle subfields, but not the prefix subfield. 

### 前缀查询优化

对根字段或其任何子字段进行"前缀"查询时，查询将被重写为"._index_prefix"子字段上的"term"查询。这比典型的文本字段上的"前缀"查询更有效，因为每个带状疱疹的一定长度的前缀直接索引为"._index_prefix"子字段中的术语。

"._index_prefix"子字段的分析器稍微修改了带状疱疹构建行为，以索引字段值末尾的术语前缀，这些术语通常不会作为带状疱疹生成。例如，如果将值"快速棕色狐狸"索引到"search_as_you_type"字段中，其中"max_shingle_size"为 3，则"棕色狐狸"和"狐狸"的前缀也会索引到"._index_prefix"子字段中，即使它们在"._3gram"子字段中未显示为术语。这允许完成字段输入中的所有术语。

[« Rank features field type](rank-features.md) [Shape field type
»](shape.md)

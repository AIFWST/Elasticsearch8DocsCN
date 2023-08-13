

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md)

[« Explore your data with runtime fields](runtime-examples.md) [Aggregate
metric field type »](aggregate-metric-double.md)

## 字段数据类型

每个字段都有一个_field数据type_或_field type_。此类型指示字段包含的数据类型(如字符串或布尔值)及其预期用途。例如，您可以将字符串索引到"文本"和"关键字"字段。但是，将分析"文本"字段值以进行全文搜索，而"关键字"字符串将保持原样以进行筛选和排序。

字段类型按 _family_ 分组。同一系列中的类型具有完全相同的搜索行为，但可能具有不同的空间使用情况或性能特征。

目前，有两种类型系列，"关键字"和"文本"。其他类型族只有一个字段类型。例如，"布尔"类型系列由一种字段类型组成："布尔"。

#### 通用类型

"二进制"

     Binary value encoded as a Base64 string. 
[`boolean`](boolean.html "Boolean field type")

     `true` and `false` values. 
[Keywords](keyword.html "Keyword type family")

     The keyword family, including `keyword`, `constant_keyword`, and `wildcard`. 
[Numbers](number.html "Numeric field types")

     Numeric types, such as `long` and `double`, used to express amounts. 
Dates

     Date types, including [`date`](date.html "Date field type") and [`date_nanos`](date_nanos.html "Date nanoseconds field type"). 
[`alias`](field-alias.html "Alias field type")

     Defines an alias for an existing field. 

#### 对象和关系类型

"对象"

     A JSON object. 
[`flattened`](flattened.html "Flattened field type")

     An entire JSON object as a single field value. 
[`nested`](nested.html "Nested field type")

     A JSON object that preserves the relationship between its subfields. 
[`join`](parent-join.html "Join field type")

     Defines a parent/child relationship for documents in the same index. 

#### 结构化数据类型

范围

     Range types, such as `long_range`, `double_range`, `date_range`, and `ip_range`. 
[`ip`](ip.html "IP field type")

     IPv4 and IPv6 addresses. 
[`version`](version.html "Version field type")

     Software versions. Supports [Semantic Versioning](https://semver.org/) precedence rules. 
[`murmur3`](/guide/en/elasticsearch/plugins/8.9/mapper-murmur3.html)

     Compute and stores hashes of values. 

#### 聚合数据类型

"aggregate_metric_double"

     Pre-aggregated metric values. 
[`histogram`](histogram.html "Histogram field type")

     Pre-aggregated numerical values in the form of a histogram. 

#### 文本搜索类型

"文本"字段

     The text family, including `text` and `match_only_text`. Analyzed, unstructured text. 
[`annotated-text`](/guide/en/elasticsearch/plugins/8.9/mapper-annotated-
text.html)

     Text containing special markup. Used for identifying named entities. 
[`completion`](search-suggesters.html#completion-suggester "Completion
Suggester")

     Used for auto-complete suggestions. 
[`search_as_you_type`](search-as-you-type.html "Search-as-you-type field
type")

     `text`-like type for as-you-type completion. 
[`token_count`](token-count.html "Token count field type")

     A count of tokens in a text. 

#### 文档排名类型

"dense_vector"

     Records dense vectors of float values. 
[`rank_feature`](rank-feature.html "Rank feature field type")

     Records a numeric feature to boost hits at query time. 
[`rank_features`](rank-features.html "Rank features field type")

     Records numeric features to boost hits at query time. 

#### 空间数据类型

"geo_point"

     Latitude and longitude points. 
[`geo_shape`](geo-shape.html "Geoshape field type")

     Complex shapes, such as polygons. 
[`point`](point.html "Point field type")

     Arbitrary cartesian points. 
[`shape`](shape.html "Shape field type")

     Arbitrary cartesian geometries. 

#### 其他类型

"渗滤器"

     Indexes queries written in [Query DSL](query-dsl.html "Query DSL"). 

###Arrays

在 Elasticsearch 中，数组不需要专用的字段数据类型。默认情况下，任何字段都可以包含零个或多个值，但是，数组中的所有值必须具有相同的字段类型。请参阅数组。

### 多字段

出于不同的目的，以不同的方式为同一字段编制索引通常很有用。例如，可以将"字符串"字段映射为全文搜索的"文本"字段，以及用于排序或聚合的"关键字"字段。或者，您可以使用"标准"分析器、"英语"分析器和"法语"分析器为文本字段编制索引。

这就是_multi-fields_的目的。大多数字段类型通过"字段"参数支持多字段。

[« Explore your data with runtime fields](runtime-examples.md) [Aggregate
metric field type »](aggregate-metric-double.md)

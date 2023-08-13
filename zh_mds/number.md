

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Nested field type](nested.md) [Object field type »](object.md)

## 数值字段类型

支持以下数值类型：

`long`

|

有符号的 64 位整数，最小值为"-263"，最大值为"263-1"。   ---|--- "整数"

|

有符号 32 位整数，最小值为"-231"，最大值为"231-1"。   "短"

|

有符号的 16 位整数，最小值为"-32，768"，最大值为"32，767"。   "字节"

|

有符号 8 位整数，最小值为"-128"，最大值为"127"。   "双"

|

双精度 64 位 IEEE 754 浮点数，限制为有限值。   "浮动"

|

单精度 32 位 IEEE 754 浮点数，限制为有限值。   "half_float"

|

半精度 16 位 IEEE 754 浮点数，限制为有限值。   "scaled_float"

|

由"长整型"支持的浮点数，由固定的"双倍"缩放因子缩放。   "unsigned_long"

|

一个无符号的 64 位整数，最小值为 0，最大值为"264-1"。   下面是使用数值字段配置映射的示例：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            number_of_bytes: {
              type: 'integer'
            },
            time_in_seconds: {
              type: 'float'
            },
            price: {
              type: 'scaled_float',
              scaling_factor: 100
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Indices.Create(
    	"my-index-000001",
    	es.Indices.Create.WithBody(strings.NewReader(`{
    	  "mappings": {
    	    "properties": {
    	      "number_of_bytes": {
    	        "type": "integer"
    	      },
    	      "time_in_seconds": {
    	        "type": "float"
    	      },
    	      "price": {
    	        "type": "scaled_float",
    	        "scaling_factor": 100
    	      }
    	    }
    	  }
    	}`)),
    )
    fmt.Println(res, err)
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "number_of_bytes": {
            "type": "integer"
          },
          "time_in_seconds": {
            "type": "float"
          },
          "price": {
            "type": "scaled_float",
            "scaling_factor": 100
          }
        }
      }
    }

"双精度"、"浮点数"和"half_float"类型认为"-0.0"和"+0.0"是不同的值。因此，对"-0.0"执行"term"查询不会与"+0.0"匹配，反之亦然。范围查询也是如此：如果上限为"-0.0"，则"+0.0"将不匹配，如果下限为"+0.0"，则"-0.0"将不匹配。

### 我应该使用哪种类型？

就整数类型("字节"，"短"，"整数"和"长")而言，您应该选择适合您的用例的最小类型。这将有助于提高索引和搜索的效率。但请注意，存储是根据存储的实际值优化的，因此选择一种类型而不是另一种类型不会影响存储要求。

对于浮点类型，使用比例因子将浮点数据存储到整数中通常更有效，这就是"scaled_float"类型在后台的作用。例如，"价格"字段可以存储在"scaled_float"中，scaling_factor为"100"。所有 API 的工作方式都像字段存储为双精度一样，但在后台，Elasticsearch 将使用美分数"price*100"，这是一个整数。这主要有助于节省磁盘空间，因为整数比浮点更容易压缩。"scaled_float"也可以使用，以换取磁盘空间的准确性。例如，假设您正在跟踪 cpu利用率作为"0"和"1"之间的数字。CPU 利用率是"12.7%"还是"13%"通常无关紧要，因此您可以使用"scaling_factor"为"100"的"scaled_float"，以便将 CPU 利用率舍入到最接近的百分比以节省空间。

如果"scaled_float"不太合适，那么您应该在浮点类型中选择足以满足用例的最小类型："双精度"、"浮点"和"half_float"。下表比较了这些类型，以帮助做出决定。

类型 |最小值 |最大值 |有效位/位数 |精度损失示例 ---|---|---|---|--- 'double'

|

`2-1074`

|

`(2-2-52)·21023`

|

'53' / '15.95'

|

'1.2345678912345678'-> '1.234567891234568' 'float'

|

`2-149`

|

`(2-2-23)·2127`

|

'24' / '7.22'

|

'1.23456789'-> '1.2345679' 'half_float'

|

`2-24`

|

`65504`

|

'11' / '3.31'

|

'1.2345'-> '1.234375' ### 映射数字标识符

并非所有数值数据都应映射为数值字段数据类型。Elasticsearch 为"range"查询优化数值字段，例如"整数"或"long"。但是，"关键字"字段更适合"术语"和其他术语级查询。

标识符(如 ISBN 或产品 ID)很少在"范围"查询中使用。但是，它们通常使用术语级查询进行检索。

在以下情况下，请考虑将数字标识符映射为"关键字"：

* 您不打算使用"范围"查询搜索标识符数据。  * 快速检索很重要。对"关键字"字段的"术语"查询搜索通常比对数值字段的"术语"搜索更快。

如果不确定要使用哪个，可以使用多字段将数据映射为"关键字"_和_数字数据类型。

### 数值字段的参数

数值类型接受以下参数：

"胁迫"

     Try to convert strings to numbers and truncate fractions for integers. Accepts `true` (default) and `false`. Not applicable for `unsigned_long`. Note that this cannot be set if the `script` parameter is used. 
[`doc_values`](doc-values.html "doc_values")

     Should the field be stored on disk in a column-stride fashion, so that it can later be used for sorting, aggregations, or scripting? Accepts `true` (default) or `false`. 
[`ignore_malformed`](ignore-malformed.html "ignore_malformed")

     If `true`, malformed numbers are ignored. If `false` (default), malformed numbers throw an exception and reject the whole document. Note that this cannot be set if the `script` parameter is used. 
[`index`](mapping-index.html "index")

     Should the field be quickly searchable? Accepts `true` (default) and `false`. Numeric fields that only have [`doc_values`](doc-values.html "doc_values") enabled can also be queried, albeit slower. 
[`meta`](mapping-field-meta.html "meta")

     Metadata about the field. 
[`null_value`](null-value.html "null_value")

     Accepts a numeric value of the same `type` as the field which is substituted for any explicit `null` values. Defaults to `null`, which means the field is treated as missing. Note that this cannot be set if the `script` parameter is used. 
`on_script_error`

     Defines what to do if the script defined by the `script` parameter throws an error at indexing time. Accepts `fail` (default), which will cause the entire document to be rejected, and `continue`, which will register the field in the document's [`_ignored`](mapping-ignored-field.html "_ignored field") metadata field and continue indexing. This parameter can only be set if the `script` field is also set. 
`script`

     If this parameter is set, then the field will index values generated by this script, rather than reading the values directly from the source. If a value is set for this field on the input document, then the document will be rejected with an error. Scripts are in the same format as their [runtime equivalent](runtime-mapping-fields.html "Map a runtime field"). Scripts can only be configured on `long` and `double` field types. 
[`store`](mapping-store.html "store")

     Whether the field value should be stored and retrievable separately from the [`_source`](mapping-source-field.html "_source field") field. Accepts `true` or `false` (default). 
`time_series_dimension`

    

(可选，布尔值)

将字段标记为时序维度。默认为"假"。

"index.mapping.dimension_fields.limit"索引设置可限制索引中的维度数。

维度字段具有以下约束：

* "doc_values"和"索引"映射参数必须为"true"。  * 字段值不能是数组或多值。

在数值字段类型中，只有"字节"、"短"、"整数"、"长"和"unsigned_long"字段支持此参数。

数值字段不能既是时序维度又是时序度量。

`time_series_metric`

    

(可选，字符串)将字段标记为时序指标。该值是指标类型。您无法更新现有字段的此参数。

数值字段的有效"time_series_metric"值

`counter`

     A cumulative metric that only monotonically increases or resets to `0` (zero). For example, a count of errors or completed tasks. 
`gauge`

     A metric that represents a single numeric that can arbitrarily increase or decrease. For example, a temperature or available disk space. 
`null` (Default)

     Not a time series metric. 

对于数值时间序列指标，"doc_values"参数必须为"true"。数值字段不能既是时序维度又是时序指标。

### scaled_float"的参数

"scaled_float"接受附加参数：

`scaling_factor`

|

编码值时要使用的比例因子。值将在索引时乘以此因子，并四舍五入到最接近的多头值。例如，scaling_factor"为"10"的"scaled_float"将在内部将"2.34"存储为"23"，并且所有搜索时操作(查询、聚合、排序)的行为都好像文档的值为"2.3"。高值"scaling_factor"不仅提高了精度，但也增加了空间要求。此参数是必需的。   ---|--- ### 合成'_source'编辑

合成"_source"仅对 TSDB 索引(将"index.mode"设置为"time_series"的索引)正式发布。对于其他指数，合成"_source"处于技术预览状态。技术预览版中的功能可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

除"unsigned_long"之外的所有数值字段在其默认配置中都支持合成"_source"。合成"_source"不能与"ignore_malformed"、"copy_to"一起使用，也不能禁用"doc_values"。

合成源始终对数值字段进行排序。例如：

    
    
    response = client.indices.create(
      index: 'idx',
      body: {
        mappings: {
          _source: {
            mode: 'synthetic'
          },
          properties: {
            long: {
              type: 'long'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'idx',
      id: 1,
      body: {
        long: [
          0,
          0,
          -123_466,
          87_612
        ]
      }
    )
    puts response
    
    
    PUT idx
    {
      "mappings": {
        "_source": { "mode": "synthetic" },
        "properties": {
          "long": { "type": "long" }
        }
      }
    }
    PUT idx/_doc/1
    {
      "long": [0, 0, -123466, 87612]
    }

将成为：

    
    
    {
      "long": [-123466, 0, 0, 87612]
    }

缩放浮点数将始终应用其比例因子，以便：

    
    
    response = client.indices.create(
      index: 'idx',
      body: {
        mappings: {
          _source: {
            mode: 'synthetic'
          },
          properties: {
            f: {
              type: 'scaled_float',
              scaling_factor: 0.01
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'idx',
      id: 1,
      body: {
        f: 123
      }
    )
    puts response
    
    
    PUT idx
    {
      "mappings": {
        "_source": { "mode": "synthetic" },
        "properties": {
          "f": { "type": "scaled_float", "scaling_factor": 0.01 }
        }
      }
    }
    PUT idx/_doc/1
    {
      "f": 123
    }

将成为：

    
    
    {
      "f": 100.0
    }

[« Nested field type](nested.md) [Object field type »](object.md)

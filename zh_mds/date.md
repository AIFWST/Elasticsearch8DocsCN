

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Completion field type](completion.md) [Date nanoseconds field type
»](date_nanos.md)

## 日期字段类型

JSON 没有日期数据类型，因此 Elasticsearch 中的日期可以是：

* 包含格式化日期的字符串，例如""2015-01-01"或""2015/01/01 12：10：30"。  * 一个数字，代表自epoch_以来的_milliseconds。  * 一个数字，表示自epoch_以来_seconds(配置)。

在内部，日期将转换为 UTC(如果指定了时区)并存储为表示自纪元以来的毫秒的长数字。

使用date_nanos字段类型如果预期为纳秒分辨率。

对日期的查询在内部转换为对此长表示形式的范围查询，并且聚合和存储字段的结果将转换回字符串，具体取决于与字段关联的日期格式。

日期将始终呈现为字符串，即使它们最初在 JSON 文档中提供为长。

可以自定义日期格式，但如果未指定"格式"，则使用默认值：

    
    
        "strict_date_optional_time||epoch_millis"

这意味着它将接受带有可选时间戳的日期，这些时间戳符合"strict_date_optional_time"或自纪元以来的毫秒支持的格式。

例如：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            date: {
              type: 'date'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        date: '2015-01-01'
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      body: {
        date: '2015-01-01T12:10:30Z'
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 3,
      body: {
        date: 1_420_070_400_001
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        sort: {
          date: 'asc'
        }
      }
    )
    puts response
    
    
    {
    	res, err := es.Indices.Create(
    		"my-index-000001",
    		es.Indices.Create.WithBody(strings.NewReader(`{
    	  "mappings": {
    	    "properties": {
    	      "date": {
    	        "type": "date"
    	      }
    	    }
    	  }
    	}`)),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Index(
    		"my-index-000001",
    		strings.NewReader(`{
    	  "date": "2015-01-01"
    	} `),
    		es.Index.WithDocumentID("1"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Index(
    		"my-index-000001",
    		strings.NewReader(`{
    	  "date": "2015-01-01T12:10:30Z"
    	} `),
    		es.Index.WithDocumentID("2"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Index(
    		"my-index-000001",
    		strings.NewReader(`{
    	  "date": 1420070400001
    	} `),
    		es.Index.WithDocumentID("3"),
    		es.Index.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    {
    	res, err := es.Search(
    		es.Search.WithIndex("my-index-000001"),
    		es.Search.WithBody(strings.NewReader(`{
    	  "sort": {
    	    "date": "asc"
    	  }
    	}`)),
    		es.Search.WithPretty(),
    	)
    	fmt.Println(res, err)
    }
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "date": {
            "type": "date" __}
        }
      }
    }
    
    PUT my-index-000001/_doc/1
    { "date": "2015-01-01" } __PUT my-index-000001/_doc/2
    { "date": "2015-01-01T12:10:30Z" } __PUT my-index-000001/_doc/3
    { "date": 1420070400001 } __GET my-index-000001/_search
    {
      "sort": { "date": "asc"} __}

__

|

"日期"字段使用默认的"格式"。   ---|---    __

|

本文档使用纯日期。   __

|

本文档包括一个时间。   __

|

本文档使用自纪元以来的毫秒。   __

|

请注意，返回的"sort"值均以自纪元以来的毫秒为单位。   日期将接受带有小数点的数字，例如"{"date"：1618249875.123456}"，但在某些情况下(#70085)，我们会在这些日期上失去精度，因此应避免使用它们。

### 多种日期格式

可以通过用"||' 作为分隔符。将依次尝试每种格式，直到找到匹配的格式。第一种格式将用于将自epoch_以来_milliseconds值转换回字符串。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            date: {
              type: 'date',
              format: 'yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis'
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
    	      "date": {
    	        "type": "date",
    	        "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
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
          "date": {
            "type":   "date",
            "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
          }
        }
      }
    }

### "日期"字段的参数

"日期"字段接受以下参数：

"doc_values"

|

字段是否应以列步幅方式存储在磁盘上，以便以后可用于排序、聚合或脚本编写？接受"真"(默认值)或"假"。   ---|---"格式"

|

可以分析的日期格式。默认为'strict_date_optional_time||epoch_millis'。   "区域设置"

|

分析日期时使用的区域设置，因为月份在所有语言中都没有相同的名称和/或缩写。默认值为"根"区域设置，"ignore_malformed"

|

如果为"true"，则忽略格式错误的数字。如果为"false"(默认值)，则格式不正确的数字会引发异常并拒绝整个文档。请注意，如果使用"script"参数，则无法设置此选项。   "索引"

|

该字段是否应该快速搜索？接受"真"(默认值)和"假"。也可以查询仅启用了"doc_values"的日期字段，尽管速度较慢。   "null_value"

|

接受配置的"格式"之一的日期值作为替换任何显式"null"值的字段。默认为"null"，表示该字段被视为缺失。请注意，这不能设置为"脚本"参数。   "on_script_error"

|

定义当由"script"参数定义的脚本在索引时引发错误时要执行的操作。接受"fail"(默认)，这将导致整个文档被拒绝，以及"继续"，这将在文档的"_ignored"元数据字段中注册字段并继续索引。仅当还设置了"脚本"字段时，才能设置此参数。   "脚本"

|

如果设置了此参数，则字段将索引此脚本生成的值，而不是直接从源读取值。如果在输入文档上为此字段设置了值，则该文档将被拒绝并显示错误。脚本的格式与其运行时等效的格式相同，并且应发出长值时间戳。   "商店"

|

字段值是否应与"_source"字段分开存储和检索。接受"真"或"假"(默认值)。   "元"

|

有关字段的元数据。   ### 纪元秒编辑

如果您需要将日期发送为自epoch_以来_seconds，请确保"格式"列出"epoch_second"：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            date: {
              type: 'date',
              format: 'strict_date_optional_time||epoch_second'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 'example',
      refresh: true,
      body: {
        date: 1_618_321_898
      }
    )
    puts response
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        fields: [
          {
            field: 'date'
          }
        ],
        _source: false
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "date": {
            "type":   "date",
            "format": "strict_date_optional_time||epoch_second"
          }
        }
      }
    }
    
    PUT my-index-000001/_doc/example?refresh
    { "date": 1618321898 }
    
    POST my-index-000001/_search
    {
      "fields": [ {"field": "date"}],
      "_source": false
    }

这将回复如下日期：

    
    
    {
      "hits": {
        "hits": [
          {
            "_id": "example",
            "_index": "my-index-000001",
            "_score": 1.0,
            "fields": {
              "date": ["2021-04-13T13:51:38.000Z"]
            }
          }
        ]
      }
    }

### 合成的"_source"

合成"_source"仅对 TSDB 索引(将"index.mode"设置为"time_series"的索引)正式发布。对于其他指数，合成"_source"处于技术预览状态。技术预览版中的功能可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

"日期"字段在其默认配置中支持合成的"_source"。合成"_source"不能与"copy_to"、"ignore_malformed"设置为 true 或禁用"doc_values"一起使用。

合成源始终对"日期"字段进行排序。例如：

    
    
    response = client.indices.create(
      index: 'idx',
      body: {
        mappings: {
          _source: {
            mode: 'synthetic'
          },
          properties: {
            date: {
              type: 'date'
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
        date: [
          '2015-01-01T12:10:30Z',
          '2014-01-01T12:10:30Z'
        ]
      }
    )
    puts response
    
    
    PUT idx
    {
      "mappings": {
        "_source": { "mode": "synthetic" },
        "properties": {
          "date": { "type": "date" }
        }
      }
    }
    PUT idx/_doc/1
    {
      "date": ["2015-01-01T12:10:30Z", "2014-01-01T12:10:30Z"]
    }

将成为：

    
    
    {
      "date": ["2014-01-01T12:10:30.000Z", "2015-01-01T12:10:30.000Z"]
    }

[« Completion field type](completion.md) [Date nanoseconds field type
»](date_nanos.md)

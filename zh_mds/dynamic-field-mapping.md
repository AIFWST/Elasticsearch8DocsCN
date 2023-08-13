

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Dynamic mapping](dynamic-mapping.md)

[« Dynamic mapping](dynamic-mapping.md) [Dynamic templates »](dynamic-
templates.md)

## 动态字段映射

当 Elasticsearch 检测到文档中的新字段时，默认情况下它会_动态_将该字段添加到类型映射中。"动态"参数控制此行为。

你可以显式指示 Elasticsearch 根据传入的文档动态创建字段，方法是将"dynamic"参数设置为"true"或"runtime"。启用动态字段映射后，Elasticsearch 将使用下表中的规则来确定如何映射每个字段的数据类型。

下表中的字段数据类型是 Elasticsearch 动态检测的唯一字段数据类型。必须显式映射所有其他数据类型。

|

**Elasticsearch数据类型** ---|--- **JSON数据类型**

|

**`"dynamic":"true"`**

|

**'"动态"："运行时"'** 'null'

|

未添加字段

|

没有添加"真"或"假"字段

|

`boolean`

|

"布尔值""双精度"

|

`float`

|

"双""长"

|

`long`

|

"长""对象"

|

`object`

|

未添加"数组"字段

|

取决于数组中的第一个非"空"值

|

取决于通过日期检测的数组"字符串"中的第一个非"null"值

|

`date`

|

通过数字检测的"日期""字符串"

|

"浮动"或"多头"

|

未通过"日期"检测或"数字"检测的"双精度"或"长""字符串"

|

带有".关键字"子字段的"文本"

|

"关键字" 您可以在文档和"对象"级别禁用动态映射。将"dynamic"参数设置为"false"会忽略新字段，如果Elasticsearch遇到未知字段，则"strict"会拒绝文档。

使用更新映射 API 更新现有字段上的"动态"设置。

您可以自定义日期检测和数字检测的动态字段映射规则。要定义可应用于其他动态字段的自定义映射规则，请使用"dynamic_templates"。

### 日期检测

如果启用了"date_detection"(默认)，则会检查新的字符串字段以查看其内容是否与"dynamic_date_formats"中指定的任何日期模式匹配。如果找到匹配项，则会添加具有相应格式的新"日期"字段。

"dynamic_date_formats"的默认值为：

['"strict_date_optional_time"'，'"yyyy/MM/dd HH：mm：ss Z||年/月/日Z"']

例如：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        create_date: '2015/09/02'
      }
    )
    puts response
    
    response = client.indices.get_mapping(
      index: 'my-index-000001'
    )
    puts response
    
    
    PUT my-index-000001/_doc/1
    {
      "create_date": "2015/09/02"
    }
    
    GET my-index-000001/_mapping __

__

|

"create_date"字段已添加为"日期"字段，格式为：""yyyy/MM/dd HH：mm：ss Z||年/月/日Z"'。   ---|--- #### 禁用日期检测编辑

可以通过将"date_detection"设置为"false"来禁用动态日期检测：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          date_detection: false
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        create_date: '2015/09/02'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "date_detection": false
      }
    }
    
    PUT my-index-000001/_doc/1 __{
      "create_date": "2015/09/02"
    }

__

|

"create_date"字段已添加为"文本"字段。   ---|--- #### 自定义检测到的日期格式编辑

或者，可以自定义"dynamic_date_formats"以支持您自己的日期格式：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          dynamic_date_formats: [
            'MM/dd/yyyy'
          ]
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        create_date: '09/25/2015'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "dynamic_date_formats": ["MM/dd/yyyy"]
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "create_date": "09/25/2015"
    }

配置日期模式数组与在由"|| "分隔的单个字符串中配置多个模式之间存在差异`.配置日期模式数组时，与第一个文档中的日期与未映射日期字段匹配的模式将确定该字段的映射：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          dynamic_date_formats: [
            'yyyy/MM',
            'MM/dd/yyyy'
          ]
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        create_date: '09/25/2015'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "dynamic_date_formats": [ "yyyy/MM", "MM/dd/yyyy"]
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "create_date": "09/25/2015"
    }

生成的映射将是：

    
    
    {
      "my-index-000001": {
        "mappings": {
          "dynamic_date_formats": [
            "yyyy/MM",
            "MM/dd/yyyy"
          ],
          "properties": {
            "create_date": {
              "type": "date",
              "format": "MM/dd/yyyy"
            }
          }
        }
      }
    }

在单个字符串中配置多个模式，以 '||' 在支持任何日期格式的映射中生成结果。这使您能够为使用不同格式的文档编制索引：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          dynamic_date_formats: [
            'yyyy/MM||MM/dd/yyyy'
          ]
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        create_date: '09/25/2015'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "dynamic_date_formats": [ "yyyy/MM||MM/dd/yyyy"]
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "create_date": "09/25/2015"
    }

生成的映射将是：

    
    
    {
      "my-index-000001": {
        "mappings": {
          "dynamic_date_formats": [
            "yyyy/MM||MM/dd/yyyy"
          ],
          "properties": {
            "create_date": {
              "type": "date",
              "format": "yyyy/MM||MM/dd/yyyy"
            }
          }
        }
      }
    }

新纪元格式("epoch_millis"和"epoch_second")不支持作为动态日期格式。

### 数字检测

虽然 JSON 支持本机浮点和整数数据类型，但某些应用程序或语言有时可能会将数字呈现为字符串。通常正确的解决方案是显式映射这些字段，但可以启用数字检测(默认情况下禁用)以自动执行此操作：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          numeric_detection: true
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        my_float: '1.0',
        my_integer: '1'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "numeric_detection": true
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "my_float":   "1.0", __"my_integer": "1" __}

__

|

"my_float"字段将添加为"浮点"字段。   ---|---    __

|

"my_integer"字段将添加为"长"字段。   « 动态映射 动态模板 »
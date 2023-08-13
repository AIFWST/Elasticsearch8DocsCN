

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Dynamic mapping](dynamic-mapping.md)

[« Dynamic field mapping](dynamic-field-mapping.md) [Explicit mapping
»](explicit-mapping.md)

## 动态模板

动态模板允许您更好地控制 Elasticsearch 如何在默认动态字段映射规则之外映射您的数据。您可以通过将动态参数设置为"true"或"运行时"来启用动态映射。然后，您可以使用动态模板定义可基于匹配条件应用于动态添加字段的自定义映射：

* "match_mapping_type"对 Elasticsearch 检测到的数据类型进行操作 * "match"和"unmatch"使用模式对字段名称进行匹配 * "path_match"和"path_unmatch"在字段的完整虚线路径上运行 * 如果动态模板未定义"match_mapping_type"、"匹配"或"path_match"，则它不会匹配任何字段。您仍然可以在批量请求的"dynamic_templates"部分中按名称引用模板。

使用映射规范中的"{name}"和"{dynamic_type}"模板变量作为占位符。

仅当字段包含具体值时，才会添加动态字段映射。当字段包含"null"或空数组时，Elasticsearch 不会添加动态字段映射。如果在"dynamic_template"中使用了"null_value"选项，则只有在为该字段具有具体值的第一个文档编制索引后，才会应用该选项。

动态模板被指定为命名对象的数组：

    
    
      "dynamic_templates": [
        {
          "my_template_name": { __... match conditions ... __"mapping": { ... } __}
        },
        ...
      ]

__

|

模板名称可以是任何字符串值。   ---|---    __

|

匹配条件可以包括以下任何一项："match_mapping_type"、"匹配"、"match_pattern"、"不匹配"、"path_match"、"path_unmatch"。   __

|

匹配字段应使用的映射。   ### 验证动态模板编辑

如果提供的映射包含无效的映射代码段，则会返回验证错误。在索引时应用动态模板时，以及在大多数情况下，在更新动态模板时，都会进行验证。在某些情况下，提供无效的映射代码段可能会导致动态模板的更新或验证失败：

* 如果未指定"match_mapping_type"，但模板对至少一种预定义映射类型有效，则映射代码段被视为有效。但是，如果与模板匹配的字段作为其他类型编制索引，则会在索引时返回验证错误。例如，配置没有"match_mapping_type"的动态模板被视为有效的字符串类型，但如果与动态模板匹配的字段被索引为长整型，则会在索引时返回验证错误。建议将"match_mapping_type"配置为预期的 JSON 类型，或在映射代码段中配置所需的"类型"。  * 如果在映射代码段中使用了"{name}"占位符，则在更新动态模板时会跳过验证。这是因为当时字段名称未知。相反，在索引时应用模板时，将进行验证。

模板按顺序处理 - 第一个匹配的模板获胜。通过更新映射 API 放置新的动态模板时，将覆盖所有现有模板。这允许在最初添加动态模板后对其进行重新排序或删除。

### 在动态模板中映射运行时字段

如果您希望 Elasticsearch 将某种类型的新字段动态映射为运行时字段，请在索引映射中设置 '"dynamic"："runtime"。这些字段不编制索引，在查询时从"_source"加载。

或者，您可以使用默认动态映射规则，然后创建动态模板将特定字段映射为运行时字段。在索引映射中设置"动态"："true"，然后创建一个动态模板以将特定类型的新字段映射为运行时字段。

假设您有每个字段都以"ip_"开头的数据。基于动态映射规则，Elasticsearch 将通过"数字"检测的任何"字符串"映射为"浮点数"或"长整型"。但是，您可以创建一个动态模板，将新字符串映射为类型为"ip"的运行时字段。

以下请求定义了一个名为"strings_as_ip"的动态模板。当Elasticsearch检测到与"ip*"模式匹配的新"字符串"字段时，它会将这些字段映射为类型为"ip"的运行时字段。由于"ip"字段不是动态映射的，因此您可以将此模板与"动态"："true"或"动态"："运行时"一起使用。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          dynamic_templates: [
            {
              strings_as_ip: {
                match_mapping_type: 'string',
                match: 'ip*',
                runtime: {
                  type: 'ip'
                }
              }
            }
          ]
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/
    {
      "mappings": {
        "dynamic_templates": [
          {
            "strings_as_ip": {
              "match_mapping_type": "string",
              "match": "ip*",
              "runtime": {
                "type": "ip"
              }
            }
          }
        ]
      }
    }

有关如何使用动态模板将"字符串"字段映射为索引字段或运行时字段的信息，请参阅此示例。

###'match_mapping_type'

"match_mapping_type"是 JSON 解析器检测到的数据类型。由于 JSON 不区分"长"和"整数"或"双精度"与"浮点数"，因此任何解析的浮点数都被视为"双精度"JSON 数据类型，而任何解析的"整数"数字都被视为"长整型"。

使用动态映射，Elasticsearch 将始终选择更广泛的数据类型。一个例外是"float"，它比"double"需要更少的存储空间，并且对于大多数应用程序来说足够精确。运行时字段不支持"float"，这就是为什么"动态"："运行时"使用"double"的原因。

Elasticsearch 会自动检测以下数据类型：

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

"关键字" 使用通配符 ("*") 匹配所有数据类型。

例如，如果我们想将所有整数字段映射为"整数"而不是"long"，将所有"字符串"字段映射为"文本"和"关键字"，我们可以使用以下模板：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          dynamic_templates: [
            {
              integers: {
                match_mapping_type: 'long',
                mapping: {
                  type: 'integer'
                }
              }
            },
            {
              strings: {
                match_mapping_type: 'string',
                mapping: {
                  type: 'text',
                  fields: {
                    raw: {
                      type: 'keyword',
                      ignore_above: 256
                    }
                  }
                }
              }
            }
          ]
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        my_integer: 5,
        my_string: 'Some string'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "dynamic_templates": [
          {
            "integers": {
              "match_mapping_type": "long",
              "mapping": {
                "type": "integer"
              }
            }
          },
          {
            "strings": {
              "match_mapping_type": "string",
              "mapping": {
                "type": "text",
                "fields": {
                  "raw": {
                    "type":  "keyword",
                    "ignore_above": 256
                  }
                }
              }
            }
          }
        ]
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "my_integer": 5, __"my_string": "Some string" __}

__

|

"my_integer"字段映射为"整数"。   ---|---    __

|

"my_string"字段映射为"文本"，具有"关键字"多字段。   ### "匹配"和"取消匹配"编辑

"match"参数使用一个或多个模式来匹配字段名称，而"unmatch"使用一个或多个模式来排除与"match"匹配的字段。

"match_pattern"参数调整"match"参数的行为，以支持字段名称上的完整 Java 正则表达式匹配，而不是简单的通配符。例如：

    
    
      "match_pattern": "regex",
      "match": "^profit_\d+$"

以下示例匹配名称以"long_"开头的所有"字符串"字段(以"_text"结尾的字段除外)，并将它们映射为"长"字段：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          dynamic_templates: [
            {
              longs_as_strings: {
                match_mapping_type: 'string',
                match: 'long_*',
                unmatch: '*_text',
                mapping: {
                  type: 'long'
                }
              }
            }
          ]
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        long_num: '5',
        long_text: 'foo'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "dynamic_templates": [
          {
            "longs_as_strings": {
              "match_mapping_type": "string",
              "match":   "long_*",
              "unmatch": "*_text",
              "mapping": {
                "type": "long"
              }
            }
          }
        ]
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "long_num": "5", __"long_text": "foo" __}

__

|

"long_num"字段映射为"长"。   ---|---    __

|

"long_text"字段使用默认的"字符串"映射。   您可以使用 JSON 数组为"匹配"或"不匹配"字段指定模式列表。

下一个示例匹配名称以"ip_"开头或以"_ip"结尾的所有字段，但以"一"开头或以"二"结尾的字段除外，并将它们映射为"ip"字段：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          dynamic_templates: [
            {
              ip_fields: {
                match: [
                  'ip_*',
                  '*_ip'
                ],
                unmatch: [
                  'one*',
                  '*two'
                ],
                mapping: {
                  type: 'ip'
                }
              }
            }
          ]
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index',
      id: 1,
      body: {
        one_ip: 'will not match',
        ip_two: 'will not match',
        three_ip: '12.12.12.12',
        ip_four: '13.13.13.13'
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "dynamic_templates": [
          {
            "ip_fields": {
              "match":   ["ip_*", "*_ip"],
              "unmatch": ["one*", "*two"],
              "mapping": {
                "type": "ip"
              }
            }
          }
        ]
      }
    }
    
    PUT my-index/_doc/1
    {
      "one_ip":   "will not match", __"ip_two":   "will not match", __"three_ip": "12.12.12.12", __"ip_four":  "13.13.13.13" __}

__

|

"one_ip"字段不匹配，因此使用"文本"的默认映射。   ---|---    __

|

"ip_two"字段不匹配，因此使用"文本"的默认映射。   __

|

"three_ip"字段映射为类型"ip"。   __

|

"ip_four"字段映射为类型"ip"。   ### "path_match"和"path_unmatch编辑"

"path_match"和"path_unmatch"参数的工作方式与"match"和"unmatch"相同，但在字段的完整虚线路径上运行，而不仅仅是最终名称，例如"some_object.*.some_field"。

本示例将"name"对象中所有字段的值复制到顶级"full_name"字段，但"中间"字段除外：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          dynamic_templates: [
            {
              full_name: {
                path_match: 'name.*',
                path_unmatch: '*.middle',
                mapping: {
                  type: 'text',
                  copy_to: 'full_name'
                }
              }
            }
          ]
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        name: {
          first: 'John',
          middle: 'Winston',
          last: 'Lennon'
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "dynamic_templates": [
          {
            "full_name": {
              "path_match":   "name.*",
              "path_unmatch": "*.middle",
              "mapping": {
                "type":       "text",
                "copy_to":    "full_name"
              }
            }
          }
        ]
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "name": {
        "first":  "John",
        "middle": "Winston",
        "last":   "Lennon"
      }
    }

以下示例对"path_match"和"path_unmatch"使用一组模式。

"name"对象或"user.name"对象中的任何字段的值都将复制到顶级"full_name"字段中，"中间"和"中间首字母"字段除外：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          dynamic_templates: [
            {
              full_name: {
                path_match: [
                  'name.*',
                  'user.name.*'
                ],
                path_unmatch: [
                  '*.middle',
                  '*.midinitial'
                ],
                mapping: {
                  type: 'text',
                  copy_to: 'full_name'
                }
              }
            }
          ]
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        name: {
          first: 'John',
          middle: 'Winston',
          last: 'Lennon'
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      body: {
        user: {
          name: {
            first: 'Jane',
            midinitial: 'M',
            last: 'Salazar'
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "dynamic_templates": [
          {
            "full_name": {
              "path_match":   ["name.*", "user.name.*"],
              "path_unmatch": ["*.middle", "*.midinitial"],
              "mapping": {
                "type":       "text",
                "copy_to":    "full_name"
              }
            }
          }
        ]
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "name": {
        "first":  "John",
        "middle": "Winston",
        "last":   "Lennon"
      }
    }
    
    PUT my-index-000001/_doc/2
    {
      "user": {
        "name": {
          "first":      "Jane",
          "midinitial": "M",
          "last":       "Salazar"
        }
      }
    }

请注意，除了叶字段之外，"path_match"和"path_unmatch"参数在对象路径上匹配。例如，为以下文档编制索引将导致错误，因为"path_match"设置也与无法映射为文本的对象字段"name.title"匹配：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 2,
      body: {
        name: {
          first: 'Paul',
          last: 'McCartney',
          title: {
            value: 'Sir',
            category: 'order of chivalry'
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/2
    {
      "name": {
        "first":  "Paul",
        "last":   "McCartney",
        "title": {
          "value": "Sir",
          "category": "order of chivalry"
        }
      }
    }

### 模板变量

"{name}"和"{dynamic_type}"占位符在"映射"中替换为字段名称和检测到的动态类型。以下示例将 allstring 字段设置为使用与字段同名的"分析器"，并对所有非字符串字段禁用"doc_values"：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          dynamic_templates: [
            {
              named_analyzers: {
                match_mapping_type: 'string',
                match: '*',
                mapping: {
                  type: 'text',
                  analyzer: '{name}'
                }
              }
            },
            {
              no_doc_values: {
                match_mapping_type: '*',
                mapping: {
                  type: '{dynamic_type}',
                  doc_values: false
                }
              }
            }
          ]
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        english: 'Some English text',
        count: 5
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "dynamic_templates": [
          {
            "named_analyzers": {
              "match_mapping_type": "string",
              "match": "*",
              "mapping": {
                "type": "text",
                "analyzer": "{name}"
              }
            }
          },
          {
            "no_doc_values": {
              "match_mapping_type":"*",
              "mapping": {
                "type": "{dynamic_type}",
                "doc_values": false
              }
            }
          }
        ]
      }
    }
    
    PUT my-index-000001/_doc/1
    {
      "english": "Some English text", __"count":   5 __}

__

|

"英语"字段与"英语"分析器映射为"字符串"字段。   ---|---    __

|

"计数"字段映射为禁用"doc_values"的"长"字段。   ### 动态模板示例编辑

以下是一些可能有用的动态模板示例：

#### 结构化搜索

当您设置"动态"："true"时，Elasticsearch 会将字符串字段映射为带有"关键字"子字段的"文本"字段。如果您只索引结构化内容而对全文搜索不感兴趣，则可以将 Elasticsearch 映射您的字段仅作为"关键字"字段。但是，您必须搜索已编制索引的完全相同的值才能搜索这些字段。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          dynamic_templates: [
            {
              strings_as_keywords: {
                match_mapping_type: 'string',
                mapping: {
                  type: 'keyword'
                }
              }
            }
          ]
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "dynamic_templates": [
          {
            "strings_as_keywords": {
              "match_mapping_type": "string",
              "mapping": {
                "type": "keyword"
              }
            }
          }
        ]
      }
    }

#### "仅文本"映射字符串

与前面的示例相反，如果您只关心字符串字段上的全文搜索，而不打算运行聚合、排序或精确搜索，您可以告诉 instruct Elasticsearch 将字符串映射为"文本"：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          dynamic_templates: [
            {
              strings_as_text: {
                match_mapping_type: 'string',
                mapping: {
                  type: 'text'
                }
              }
            }
          ]
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "dynamic_templates": [
          {
            "strings_as_text": {
              "match_mapping_type": "string",
              "mapping": {
                "type": "text"
              }
            }
          }
        ]
      }
    }

或者，您可以创建一个动态模板，以将字符串字段映射为映射运行时部分中的"关键字"字段。当 Elasticsearch 检测到类型为"string"的新字段时，这些字段将被创建为类型为"关键字"的运行时字段。

虽然您的"字符串"字段不会被编入索引，但它们的值存储在"_source"中，可用于搜索请求、聚合、筛选和排序。

例如，以下请求创建一个动态模板，用于将"字符串"字段映射为"关键字"类型的运行时字段。尽管"运行时"定义为空，但新的"字符串"字段将根据 Elasticsearch 用于向映射添加字段类型的动态映射规则映射为"关键字"运行时字段。任何未通过日期检测或数字检测的"字符串"都会自动映射为"关键字"：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          dynamic_templates: [
            {
              strings_as_keywords: {
                match_mapping_type: 'string',
                runtime: {}
              }
            }
          ]
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "dynamic_templates": [
          {
            "strings_as_keywords": {
              "match_mapping_type": "string",
              "runtime": {}
            }
          }
        ]
      }
    }

索引一个简单的文档：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        english: 'Some English text',
        count: 5
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/1
    {
      "english": "Some English text",
      "count":   5
    }

查看映射时，您将看到"英语"字段是"关键字"类型的运行时字段：

    
    
    response = client.indices.get_mapping(
      index: 'my-index-000001'
    )
    puts response
    
    
    GET my-index-000001/_mapping
    
    
    {
      "my-index-000001" : {
        "mappings" : {
          "dynamic_templates" : [
            {
              "strings_as_keywords" : {
                "match_mapping_type" : "string",
                "runtime" : { }
              }
            }
          ],
          "runtime" : {
            "english" : {
              "type" : "keyword"
            }
          },
          "properties" : {
            "count" : {
              "type" : "long"
            }
          }
        }
      }
    }

#### 禁用规范

规范是索引时间评分因素。如果您不关心评分(例如，如果您从不按分数对文档进行排序)，则可以禁用在索引中存储这些评分因素并节省一些空间。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          dynamic_templates: [
            {
              strings_as_keywords: {
                match_mapping_type: 'string',
                mapping: {
                  type: 'text',
                  norms: false,
                  fields: {
                    keyword: {
                      type: 'keyword',
                      ignore_above: 256
                    }
                  }
                }
              }
            }
          ]
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "dynamic_templates": [
          {
            "strings_as_keywords": {
              "match_mapping_type": "string",
              "mapping": {
                "type": "text",
                "norms": false,
                "fields": {
                  "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                  }
                }
              }
            }
          }
        ]
      }
    }

子"关键字"字段将显示在此模板中，以与动态映射的默认规则一致。当然，如果您不需要它们，因为您不需要对此字段执行精确搜索或聚合，则可以按照上一节中所述将其删除。

#### 时间序列

使用 Elasticsearch 进行时间序列分析时，通常会有许多数字字段，您通常会聚合这些字段，但从不对其进行过滤。在这种情况下，您可以禁用对这些字段的索引以节省磁盘空间，还可以获得一些索引速度：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          dynamic_templates: [
            {
              unindexed_longs: {
                match_mapping_type: 'long',
                mapping: {
                  type: 'long',
                  index: false
                }
              }
            },
            {
              unindexed_doubles: {
                match_mapping_type: 'double',
                mapping: {
                  type: 'float',
                  index: false
                }
              }
            }
          ]
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "dynamic_templates": [
          {
            "unindexed_longs": {
              "match_mapping_type": "long",
              "mapping": {
                "type": "long",
                "index": false
              }
            }
          },
          {
            "unindexed_doubles": {
              "match_mapping_type": "double",
              "mapping": {
                "type": "float", __"index": false
              }
            }
          }
        ]
      }
    }

__

|

与默认的动态映射规则一样，双精度被映射为浮点数，这些浮点数通常足够精确，但需要一半的磁盘空间。   ---|--- « 动态字段映射 显式映射»
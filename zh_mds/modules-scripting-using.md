

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Scripting](modules-scripting.md)

[« Painless scripting language](modules-scripting-painless.md) [Scripts,
caching, and search speed »](scripts-and-search-speed.md)

## 如何编写脚本

只要 Elasticsearch API 支持脚本，语法都遵循相同的模式;指定脚本的语言，提供脚本逻辑(或源)，并添加传递到脚本中的参数：

    
    
      "script": {
        "lang":   "...",
        "source" | "id": "...",
        "params": { ... }
      }

`lang`

     Specifies the language the script is written in. Defaults to `painless`. 
`source`, `id`

     The script itself, which you specify as `source` for an inline script or `id` for a stored script. Use the [stored script APIs](script-apis.html#stored-script-apis "Stored script APIs") to create and manage stored scripts. 
`params`

     Specifies any named parameters that are passed into the script as variables. [Use parameters](modules-scripting-using.html#prefer-params "Use parameters in your script") instead of hard-coded values to decrease compile time. 

### 写你的第一个脚本

Painless 是 Elasticsearch 的默认脚本语言。它是安全的，高性能的，并为任何有一点编码经验的人提供了自然的语法。

无痛脚本的结构为一个或多个语句，并且可以选择在开头具有一个或多个用户定义的函数。脚本必须始终至少有一个语句。

无痛执行 API 提供了使用简单的用户定义参数测试脚本并接收结果的能力。让我们从一个完整的脚本开始并查看其组成部分。

首先，使用单个字段为文档编制索引，以便我们有一些数据可以使用：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        my_field: 5
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/1
    {
      "my_field": 5
    }

然后，我们可以构造一个在该字段上运行的脚本，并将该脚本作为查询的一部分运行。以下查询使用搜索 API 的"script_fields"参数检索脚本评估。这里发生了很多事情，但我们将分解组件以单独理解它们。现在，您只需要了解此脚本采用"my_field"并对其进行操作。

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        script_fields: {
          my_doubled_field: {
            script: {
              source: "doc['my_field'].value * params['multiplier']",
              params: {
                multiplier: 2
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "script_fields": {
        "my_doubled_field": {
          "script": { __"source": "doc['my_field'].value * params['multiplier']", __"params": {
              "multiplier": 2
            }
          }
        }
      }
    }

__

|

"脚本"对象---|--- __

|

"script"源 "script"是一个标准的JSON对象，用于定义Elasticsearch中大多数API下的脚本。此对象需要"源"来定义脚本本身。脚本未指定语言，因此默认为"无痛"。

### 在脚本中使用参数

Elasticsearch 第一次看到新脚本时，它会编译脚本并将编译后的版本存储在缓存中。编译可能是一个繁重的过程。与其在脚本中硬编码值，不如将它们作为命名的"params"传递。

例如，在前面的脚本中，我们可以只硬编码值并编写一个看似不那么复杂的脚本。我们可以检索 'my_field' 的第一个值，然后将其乘以 '2'：

    
    
    "source": "return doc['my_field'].value * 2"

虽然它有效，但这个解决方案非常不灵活。我们必须修改脚本源代码来更改乘数，并且 Elasticsearch 必须在每次乘数更改时重新编译脚本。

使用名为"params"的"参数"来使脚本灵活，并减少脚本运行时的编译时间，而不是硬编码值。您现在可以更改"乘数"参数，而无需 Elasticsearch 重新编译脚本。

    
    
    "source": "doc['my_field'].value * params['multiplier']",
    "params": {
      "multiplier": 2
    }

默认情况下，每 5 分钟最多可以编译 150 个脚本。对于摄取上下文，默认脚本编译速率不受限制。

    
    
    script.context.field.max_compilations_rate=100/10m

如果您在短时间内编译了太多独特的脚本，Elasticsearch 会拒绝新的动态脚本，并显示"circuit_breaking_exception"错误。

### 缩短您的脚本

使用 Painless 固有的语法功能，您可以减少脚本中的每平方性并缩短它们。下面是一个简单的脚本，我们可以缩短它：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        script_fields: {
          my_doubled_field: {
            script: {
              lang: 'painless',
              source: "doc['my_field'].value * params.get('multiplier');",
              params: {
                multiplier: 2
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "script_fields": {
        "my_doubled_field": {
          "script": {
            "lang":   "painless",
            "source": "doc['my_field'].value * params.get('multiplier');",
            "params": {
              "multiplier": 2
            }
          }
        }
      }
    }

让我们看一下脚本的缩短版本，看看它比以前的迭代包含哪些改进：

    
    
    GET my-index-000001/_search
    {
      "script_fields": {
        "my_doubled_field": {
          "script": {
            "source": "field('my_field').get(null) * params['multiplier']",
            "params": {
              "multiplier": 2
            }
          }
        }
      }
    }

此版本的脚本删除了几个组件并显着简化了语法：

* "郎"声明。由于无痛是默认语言，因此在编写无痛脚本时无需指定语言。  * "返回"关键字。Painless 会自动使用脚本中的 final 语句(如果可能)在需要返回值的脚本上下文中生成返回值。  * "get"方法，替换为括号"[]"。Painless 使用专门针对"Map"类型的快捷方式，允许我们使用括号而不是更长的"get"方法。  * "源"语句末尾的分号。无痛不需要分号来表示块的最终陈述。但是，在其他情况下，它确实要求它们消除歧义。

在 Elasticsearch 支持脚本的任何地方使用此缩写语法，例如在创建运行时字段时。

### 存储和检索脚本

可以使用存储的脚本 API 从群集状态存储和检索脚本。存储脚本可减少编译时间并加快搜索速度。

与常规脚本不同，存储的脚本要求您使用"lang"参数指定脚本语言。

若要创建脚本，请使用创建存储的脚本 API。例如，以下请求创建一个名为"计算分数"的存储脚本。

    
    
    response = client.put_script(
      id: 'calculate-score',
      body: {
        script: {
          lang: 'painless',
          source: "Math.log(_score * 2) + params['my_modifier']"
        }
      }
    )
    puts response
    
    
    POST _scripts/calculate-score
    {
      "script": {
        "lang": "painless",
        "source": "Math.log(_score * 2) + params['my_modifier']"
      }
    }

可以使用获取存储的脚本 API 检索该脚本。

    
    
    response = client.get_script(
      id: 'calculate-score'
    )
    puts response
    
    
    GET _scripts/calculate-score

要在查询中使用存储的脚本，请在"script"声明中包含脚本"id"：

    
    
    response = client.search(
      index: 'my-index-000001',
      body: {
        query: {
          script_score: {
            query: {
              match: {
                message: 'some message'
              }
            },
            script: {
              id: 'calculate-score',
              params: {
                my_modifier: 2
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET my-index-000001/_search
    {
      "query": {
        "script_score": {
          "query": {
            "match": {
                "message": "some message"
            }
          },
          "script": {
            "id": "calculate-score", __"params": {
              "my_modifier": 2
            }
          }
        }
      }
    }

__

|

存储脚本的"id"---|--- 要删除存储的脚本，请提交删除存储的脚本 API 请求。

    
    
    response = client.delete_script(
      id: 'calculate-score'
    )
    puts response
    
    
    DELETE _scripts/calculate-score

### 使用脚本更新文档

您可以使用更新 API 更新具有指定脚本的文档。该脚本可以更新、删除或跳过修改文档。更新 API 还支持传递部分文档，该文档将合并到现有文档中。

首先，让我们为一个简单的文档编制索引：

    
    
    response = client.index(
      index: 'my-index-000001',
      id: 1,
      body: {
        counter: 1,
        tags: [
          'red'
        ]
      }
    )
    puts response
    
    
    PUT my-index-000001/_doc/1
    {
      "counter" : 1,
      "tags" : ["red"]
    }

若要递增计数器，可以使用以下脚本提交更新请求：

    
    
    response = client.update(
      index: 'my-index-000001',
      id: 1,
      body: {
        script: {
          source: 'ctx._source.counter += params.count',
          lang: 'painless',
          params: {
            count: 4
          }
        }
      }
    )
    puts response
    
    
    POST my-index-000001/_update/1
    {
      "script" : {
        "source": "ctx._source.counter += params.count",
        "lang": "painless",
        "params" : {
          "count" : 4
        }
      }
    }

同样，您可以使用更新脚本将标签添加到标签列表中。因为这只是一个列表，所以即使存在标签，也会添加它：

    
    
    response = client.update(
      index: 'my-index-000001',
      id: 1,
      body: {
        script: {
          source: "ctx._source.tags.add(params['tag'])",
          lang: 'painless',
          params: {
            tag: 'blue'
          }
        }
      }
    )
    puts response
    
    
    POST my-index-000001/_update/1
    {
      "script": {
        "source": "ctx._source.tags.add(params['tag'])",
        "lang": "painless",
        "params": {
          "tag": "blue"
        }
      }
    }

您还可以从标签列表中删除标签。Java'List'的'remove'方法在Painless中可用。它采用要删除的元素的索引。为避免可能的运行时错误，您首先需要确保标记存在。如果列表包含标记的重复项，则此脚本仅删除一个匹配项。

    
    
    response = client.update(
      index: 'my-index-000001',
      id: 1,
      body: {
        script: {
          source: "if (ctx._source.tags.contains(params['tag'])) { ctx._source.tags.remove(ctx._source.tags.indexOf(params['tag'])) }",
          lang: 'painless',
          params: {
            tag: 'blue'
          }
        }
      }
    )
    puts response
    
    
    POST my-index-000001/_update/1
    {
      "script": {
        "source": "if (ctx._source.tags.contains(params['tag'])) { ctx._source.tags.remove(ctx._source.tags.indexOf(params['tag'])) }",
        "lang": "painless",
        "params": {
          "tag": "blue"
        }
      }
    }

您还可以在文档中添加和删除字段。例如，此脚本添加字段"new_field"：

    
    
    response = client.update(
      index: 'my-index-000001',
      id: 1,
      body: {
        script: "ctx._source.new_field = 'value_of_new_field'"
      }
    )
    puts response
    
    
    POST my-index-000001/_update/1
    {
      "script" : "ctx._source.new_field = 'value_of_new_field'"
    }

相反，此脚本删除字段"new_field"：

    
    
    response = client.update(
      index: 'my-index-000001',
      id: 1,
      body: {
        script: "ctx._source.remove('new_field')"
      }
    )
    puts response
    
    
    POST my-index-000001/_update/1
    {
      "script" : "ctx._source.remove('new_field')"
    }

除了更新文档，您还可以更改从脚本中执行的操作。例如，如果"标签"字段包含"绿色"，则此请求将删除文档。否则它什么都不做('noop')：

    
    
    response = client.update(
      index: 'my-index-000001',
      id: 1,
      body: {
        script: {
          source: "if (ctx._source.tags.contains(params['tag'])) { ctx.op = 'delete' } else { ctx.op = 'none' }",
          lang: 'painless',
          params: {
            tag: 'green'
          }
        }
      }
    )
    puts response
    
    
    POST my-index-000001/_update/1
    {
      "script": {
        "source": "if (ctx._source.tags.contains(params['tag'])) { ctx.op = 'delete' } else { ctx.op = 'none' }",
        "lang": "painless",
        "params": {
          "tag": "green"
        }
      }
    }

[« Painless scripting language](modules-scripting-painless.md) [Scripts,
caching, and search speed »](scripts-and-search-speed.md)

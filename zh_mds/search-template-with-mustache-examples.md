

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Search your
data](search-your-data.md) ›[Search templates](search-template.md)

[« Search templates](search-template.md) [Sort search results »](sort-
search-results.md)

## 使用胡子搜索模板示例

胡须模板语言定义了您可以在模板中使用的各种标签类型。以下部分介绍了其中一些标签类型，并提供了在 Elasticsearch 搜索模板中使用它们的示例。

### 胡子变量

胡须标签通常括在双花括号中。胡须变量："{{my-variable}}"是一种胡须标签。当你运行模板化搜索时，Elasticsearch 会用来自 'params' 的值替换这些变量。

例如，请考虑以下搜索模板：

    
    
    PUT _scripts/my-search-template
    {
      "script": {
        "lang": "mustache",
        "source": {
          "query": {
            "match": {
              "message": "{{query_string}}"
            }
          },
          "from": "{{from}}",
          "size": "{{size}}"
        }
      }
    }

使用"参数"测试上面的搜索模板：

    
    
    response = client.render_search_template(
      body: {
        id: 'my-search-template',
        params: {
          query_string: 'hello world',
          from: 20,
          size: 10
        }
      }
    )
    puts response
    
    
    POST _render/template
    {
      "id": "my-search-template",
      "params": {
        "query_string": "hello world",
        "from": 20,
        "size": 10
      }
    }

渲染时，"消息"中的"{{query_string}}"将替换为"参数"中传递的"helloworld"。

    
    
    {
      "template_output": {
        "query": {
          "match": {
            "message": "hello world"
          }
        },
        "from": "20",
        "size": "10"
      }
    }

如果您的搜索模板没有将值传递给您的"query_string"，则邮件将替换为空字符串。

例如：

    
    
    POST _render/template
    {
      "id": "my-search-template",
      "params": {
        "from": 20,
        "size": 10
      }
    }

呈现时，模板输出为：

    
    
    {
      "template_output": {
        "query": {
          "match": {
            "message": ""
          }
        },
        "from": "20",
        "size": "10"
      }
    }

###Sections

部分也是一种胡须标签。您可以在搜索模板中使用带有嵌套或非嵌套对象的"部分"。节以"{{#my-section-variable}}"开头，以"{{/my-section-variable}}"结尾。

以下搜索模板显示了使用具有嵌套对象的节的示例：

    
    
    POST _render/template
    {
      "source":
      """
      {
        "query": {
          "match": {
            {{#query_message}}
              {{#query_string}}
            "message": "Hello {{#first_name_section}}{{first_name}}{{/first_name_section}} {{#last_name_section}}{{last_name}}{{/last_name_section}}"
              {{/query_string}}
            {{/query_message}}
          }
        }
      }
      """,
      "params": {
        "query_message": {
           "query_string": {
             "first_name_section": {"first_name": "John"},
             "last_name_section": {"last_name": "kimchy"}
           }
        }
      }
    }

模板呈现为：

    
    
    {
      "template_output": {
        "query": {
          "match": {
            "message": "Hello John kimchy"
          }
        }
      }
    }

####Lists

您可以传递对象列表并循环搜索模板中的每个项目。

例如，以下搜索模板合并部分并匹配所有用户名：

    
    
    PUT _scripts/my-search-template
    {
      "script": {
        "lang": "mustache",
        "source": {
          "query":{
            "multi-match":{
              "query": "{{query_string}}",
              "fields": """[{{#text_fields}}{{user_name}},{{/text_fields}}]"""
            }
          }
        }
      }
    }

测试模板：

    
    
    POST _render/template
    {
      "id": "my-search-template",
      "params": {
        "query_string": "My string",
        "text_fields": [
          {
            "user_name": "John"
          },
          {
            "user_name": "kimchy"
          }
        ]
      }
    }

呈现时，模板输出：

    
    
    {
      "template_output": {
        "query": {
          "multi-match": {
            "query": "My string",
            "fields": "[John,kimchy,]"
          }
        }
      }
    }

上述情况将导致尾随逗号问题，从而导致 JSON 无效。解决方法是包含一个倒置部分并添加一个变量以确保它是数组中的最后一项。

例如：

    
    
    PUT _scripts/my-search-template
    {
      "script": {
        "lang": "mustache",
        "source": {
          "query":{
            "multi-match":{
              "query": "{{query_string}}",
              "fields": """[{{#text_fields}}{{user_name}}{{^last}},{{/last}}{{/text_fields}}]"""
            }
          }
        }
      }
    }

使用变量再次测试"my-search-template"："last"以确定它是数组中的最后一项：

    
    
    POST _render/template
    {
      "id": "my-search-template",
      "params": {
        "query_string": "My string",
        "text_fields": [
          {
            "user_name": "John",
            "last": false
          },
          {
            "user_name": "kimchy",
            "last": true
          }
        ]
      }
    }

呈现模板输出时：

    
    
    {
      "template_output": {
        "query": {
          "multi-match": {
            "query": "My string",
            "fields": "[John,kimchy]"
          }
        }
      }
    }

####Lambdas

Elasticsearch 具有预先构建的自定义函数，以支持将文本转换为特定格式。

要了解有关胡须 lambda 用法的更多信息，请查看 Urlencode 字符串、连接值和转换为 json 中的示例。

### 倒置截面

当您想要设置一次值时，反转部分很有用。

若要使用倒置节，请使用以下语法：

    
    
    {{^my-variable}} content {{/my-variable}}

例如，在以下搜索模板中，如果"name_exists"为"false"，"message"设置为"Hello World"，否则设置为空字符串。

    
    
    POST _render/template
    {
      "source": {
        "query": {
          "match": {
            "message": "{{^name_exists}}Hello World{{/name_exists}}"
          }
        }
      },
      "params": {
         "name_exists": false
      }
    }

它们还可以与条件和默认值结合使用。

例如，在以下搜索模板中，如果"name_exists"为"true"，则会替换"{{query_string}}"的值。如果"name_exists"为"false"，则设置为默认值"World"。

    
    
    POST _render/template
    {
      "source": {
        "query": {
          "match": {
            "message": "Hello {{#name_exists}}{{query_string}}{{/name_exists}}{{^name_exists}}World{{/name_exists}}"
          }
        }
      },
      "params": {
        "query_string": "Kimchy",
         "name_exists": true
      }
    }

渲染时，模板输出：

    
    
    {
      "template_output": {
        "query": {
          "match": {
            "message": "Hello Kimchy"
          }
        }
      }
    }

### Setdelimiter

您可以将默认分隔符：双花括号"{{my-variable}}"更改为搜索模板中的任何自定义分隔符。

例如，以下搜索模板将默认分隔符更改为单个圆括号"(query_string)"。

    
    
    PUT _scripts/my-search-template
    {
      "script": {
        "lang": "mustache",
        "source":
        """
        {
          "query": {
            "match": {
               {{=( )=}}
              "message": "(query_string)"
              (={{ }}=)
            }
          }
        }
        """
      }
    }

使用新的分隔符测试模板：

    
    
    POST _render/template
    {
      "id": "my-search-template",
      "params": {
        "query_string": "hello world"
      }
    }

呈现时，模板输出：

    
    
    {
      "template_output": {
        "query": {
          "match": {
            "message": "hello world"
          }
        }
      }
    }

### 不支持的功能

以下胡须功能在 Elasticsearch 搜索模板中不受支持：

* 部分

[« Search templates](search-template.md) [Sort search results »](sort-
search-results.md)

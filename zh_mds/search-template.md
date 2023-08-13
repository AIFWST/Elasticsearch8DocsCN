

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Search your
data](search-your-data.md)

[« Search shard routing](search-shard-routing.md) [Search template examples
with Mustache »](search-template-with-mustache-examples.md)

## 搜索模板

搜索模板是可以使用不同变量运行的存储搜索。

如果使用 Elasticsearch 作为搜索后端，则可以将搜索栏中的用户输入作为搜索模板的参数传递。这使您可以运行搜索，而无需向用户公开 Elasticsearch 的查询语法。

如果您将 Elasticsearch 用于自定义应用程序，搜索模板可让您在不修改应用程序代码的情况下更改搜索。

### 创建搜索模板

若要创建或更新搜索模板，请使用创建存储的脚本 API。

请求的"source"支持与searchAPI的请求正文相同的参数."source"也接受来自开源projectmustache.java的Mustachevariables。

通常，Mustache 变量括在双大括号中："{{my-var}}"。当你运行模板化搜索时，Elasticsearch 会用 'params' 中的值替换这些变量。要了解有关胡须语法的更多信息 - 请参阅 Mustache.jsmanual 搜索模板必须使用"胡须"的"lang"。

以下请求创建一个"id"为"我的搜索模板"的搜索模板。

    
    
    response = client.put_script(
      id: 'my-search-template',
      body: {
        script: {
          lang: 'mustache',
          source: {
            query: {
              match: {
                message: '{{query_string}}'
              }
            },
            from: '{{from}}',
            size: '{{size}}'
          },
          params: {
            query_string: 'My query string'
          }
        }
      }
    )
    puts response
    
    
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
        },
        "params": {
          "query_string": "My query string"
        }
      }
    }

Elasticsearch 将搜索模板存储为集群状态下的 Mustache 脚本。Elasticsearch 在"模板"脚本上下文中编译搜索模板。限制或禁用脚本的设置也会影响搜索模板。

### 验证搜索模板

要使用不同的"参数"测试模板，请使用渲染搜索模板API。

    
    
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

呈现时，模板输出搜索请求正文。

    
    
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

您还可以使用 API 测试内联模板。

    
    
    response = client.render_search_template(
      body: {
        source: {
          query: {
            match: {
              message: '{{query_string}}'
            }
          },
          from: '{{from}}',
          size: '{{size}}'
        },
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
        "source": {
          "query": {
            "match": {
              "message": "{{query_string}}"
            }
          },
          "from": "{{from}}",
          "size": "{{size}}"
        },
      "params": {
        "query_string": "hello world",
        "from": 20,
        "size": 10
      }
    }

### 运行模板化搜索

若要使用搜索模板运行搜索，请使用搜索模板 API。您可以为每个请求指定不同的"参数"。

    
    
    response = client.search_template(
      index: 'my-index',
      body: {
        id: 'my-search-template',
        params: {
          query_string: 'hello world',
          from: 0,
          size: 10
        }
      }
    )
    puts response
    
    
    GET my-index/_search/template
    {
      "id": "my-search-template",
      "params": {
        "query_string": "hello world",
        "from": 0,
        "size": 10
      }
    }

响应使用与搜索 API 的响应相同的属性。

    
    
    {
      "took": 36,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": {
          "value": 1,
          "relation": "eq"
        },
        "max_score": 0.5753642,
        "hits": [
          {
            "_index": "my-index",
            "_id": "1",
            "_score": 0.5753642,
            "_source": {
              "message": "hello world"
            }
          }
        ]
      }
    }

### 运行多个模板化搜索

要使用单个请求运行多个模板化搜索，请使用多重搜索模板 API。与多个单独的搜索相比，这些请求通常具有更少的开销和更快的速度。

    
    
    response = client.msearch_template(
      index: 'my-index',
      body: [
        {},
        {
          id: 'my-search-template',
          params: {
            query_string: 'hello world',
            from: 0,
            size: 10
          }
        },
        {},
        {
          id: 'my-other-search-template',
          params: {
            query_type: 'match_all'
          }
        }
      ]
    )
    puts response
    
    
    GET my-index/_msearch/template
    { }
    { "id": "my-search-template", "params": { "query_string": "hello world", "from": 0, "size": 10 }}
    { }
    { "id": "my-other-search-template", "params": { "query_type": "match_all" }}

### 获取搜索模板

若要检索搜索模板，请使用获取存储的脚本 API。

    
    
    response = client.get_script(
      id: 'my-search-template'
    )
    puts response
    
    
    GET _scripts/my-search-template

若要获取所有搜索模板和其他存储脚本的列表，请使用群集状态 API。

    
    
    response = client.cluster.state(
      metric: 'metadata',
      pretty: true,
      filter_path: 'metadata.stored_scripts'
    )
    puts response
    
    
    GET _cluster/state/metadata?pretty&filter_path=metadata.stored_scripts

### 删除搜索模板

若要删除搜索模板，请使用删除存储的脚本 API。

    
    
    response = client.delete_script(
      id: 'my-search-template'
    )
    puts response
    
    
    DELETE _scripts/my-search-template

### 设置默认值

若要设置变量的默认值，请使用以下语法：

    
    
    {{my-var}}{{^my-var}}default value{{/my-var}}

如果模板化搜索未在其"参数"中指定值，则搜索将改用默认值。例如，以下模板为"发件人"和"大小"设置默认值。

    
    
    response = client.render_search_template(
      body: {
        source: {
          query: {
            match: {
              message: '{{query_string}}'
            }
          },
          from: '{{from}}{{^from}}0{{/from}}',
          size: '{{size}}{{^size}}10{{/size}}'
        },
        params: {
          query_string: 'hello world'
        }
      }
    )
    puts response
    
    
    POST _render/template
    {
      "source": {
        "query": {
          "match": {
            "message": "{{query_string}}"
          }
        },
        "from": "{{from}}{{^from}}0{{/from}}",
        "size": "{{size}}{{^size}}10{{/size}}"
      },
      "params": {
        "query_string": "hello world"
      }
    }

### 网址编码字符串

使用"{{#url}}"函数对字符串进行 URL 编码。

    
    
    response = client.render_search_template(
      body: {
        source: {
          query: {
            term: {
              "url.full": '{{#url}}{{host}}/{{page}}{{/url}}'
            }
          }
        },
        params: {
          host: 'http://example.com',
          page: 'hello-world'
        }
      }
    )
    puts response
    
    
    POST _render/template
    {
      "source": {
        "query": {
          "term": {
            "url.full": "{{#url}}{{host}}/{{page}}{{/url}}"
          }
        }
      },
      "params": {
        "host": "http://example.com",
        "page": "hello-world"
      }
    }

模板呈现为：

    
    
    {
      "template_output": {
        "query": {
          "term": {
            "url.full": "http%3A%2F%2Fexample.com%2Fhello-world"
          }
        }
      }
    }

### 连接值

使用"{{#join}}"函数将数组值连接为逗号分隔的字符串。例如，以下模板连接两个电子邮件地址。

    
    
    response = client.render_search_template(
      body: {
        source: {
          query: {
            match: {
              "user.group.emails": '{{#join}}emails{{/join}}'
            }
          }
        },
        params: {
          emails: [
            'user1@example.com',
            'user_one@example.com'
          ]
        }
      }
    )
    puts response
    
    
    POST _render/template
    {
      "source": {
        "query": {
          "match": {
            "user.group.emails": "{{#join}}emails{{/join}}"
          }
        }
      },
      "params": {
        "emails": [ "user1@example.com", "user_one@example.com" ]
      }
    }

模板呈现为：

    
    
    {
      "template_output": {
        "query": {
          "match": {
            "user.group.emails": "user1@example.com,user_one@example.com"
          }
        }
      }
    }

您还可以指定自定义分隔符。

    
    
    response = client.render_search_template(
      body: {
        source: {
          query: {
            range: {
              "user.effective.date": {
                gte: '{{date.min}}',
                lte: '{{date.max}}',
                format: "{{#join delimiter='||'}}date.formats{{/join delimiter='||'}}"
              }
            }
          }
        },
        params: {
          date: {
            min: '2098',
            max: '06/05/2099',
            formats: [
              'dd/MM/yyyy',
              'yyyy'
            ]
          }
        }
      }
    )
    puts response
    
    
    POST _render/template
    {
      "source": {
        "query": {
          "range": {
            "user.effective.date": {
              "gte": "{{date.min}}",
              "lte": "{{date.max}}",
              "format": "{{#join delimiter='||'}}date.formats{{/join delimiter='||'}}"
    	      }
          }
        }
      },
      "params": {
        "date": {
          "min": "2098",
          "max": "06/05/2099",
          "formats": ["dd/MM/yyyy", "yyyy"]
        }
      }
    }

模板呈现为：

    
    
    {
      "template_output": {
        "query": {
          "range": {
            "user.effective.date": {
              "gte": "2098",
              "lte": "06/05/2099",
              "format": "dd/MM/yyyy||yyyy"
            }
          }
        }
      }
    }

### 转换为 JSON

使用 '{{#toJson}}' 函数将变量值转换为其 JSON 表示形式。

例如，以下模板使用"{{#toJson}}"传递数组。为了确保请求正文是有效的 JSON，"源"以字符串格式写入。

    
    
    response = client.render_search_template(
      body: {
        source: '{ "query": { "terms": { "tags": {{#toJson}}tags{{/toJson}} }}}',
        params: {
          tags: [
            'prod',
            'es01'
          ]
        }
      }
    )
    puts response
    
    
    POST _render/template
    {
      "source": "{ \"query\": { \"terms\": { \"tags\": {{#toJson}}tags{{/toJson}} }}}",
      "params": {
        "tags": [
          "prod",
          "es01"
        ]
      }
    }

模板呈现为：

    
    
    {
      "template_output": {
        "query": {
          "terms": {
            "tags": [
              "prod",
              "es01"
            ]
          }
        }
      }
    }

您还可以使用"{{#toJson}}"来传递对象。

    
    
    response = client.render_search_template(
      body: {
        source: '{ "query": {{#toJson}}my_query{{/toJson}} }',
        params: {
          my_query: {
            match_all: {}
          }
        }
      }
    )
    puts response
    
    
    POST _render/template
    {
      "source": "{ \"query\": {{#toJson}}my_query{{/toJson}} }",
      "params": {
        "my_query": {
          "match_all": { }
        }
      }
    }

模板呈现为：

    
    
    {
      "template_output" : {
        "query" : {
          "match_all" : { }
        }
      }
    }

您还可以传递对象数组。

    
    
    response = client.render_search_template(
      body: {
        source: '{ "query": { "bool": { "must": {{#toJson}}clauses{{/toJson}} }}}',
        params: {
          clauses: [
            {
              term: {
                "user.id": 'kimchy'
              }
            },
            {
              term: {
                "url.domain": 'example.com'
              }
            }
          ]
        }
      }
    )
    puts response
    
    
    POST _render/template
    {
      "source": "{ \"query\": { \"bool\": { \"must\": {{#toJson}}clauses{{/toJson}} }}}",
      "params": {
        "clauses": [
          {
            "term": {
              "user.id": "kimchy"
            }
          },
          {
            "term": {
              "url.domain": "example.com"
            }
          }
        ]
      }
    }

模板呈现为：

    
    
    {
      "template_output": {
        "query": {
          "bool": {
            "must": [
              {
                "term": {
                  "user.id": "kimchy"
                }
              },
              {
                "term": {
                  "url.domain": "example.com"
                }
              }
            ]
          }
        }
      }
    }

### 使用条件

若要创建 if 条件，请使用以下语法：

    
    
    {{#condition}}content{{/condition}}

如果条件变量为"true"，则 Elasticsearch 显示其内容。例如，如果"year_scope"为"true"，则以下模板搜索过去一年的数据。

    
    
    response = client.render_search_template(
      body: {
        source: '{ "query": { "bool": { "filter": [ {{#year_scope}} { "range": { "@timestamp": { "gte": "now-1y/d", "lt": "now/d" } } }, {{/year_scope}} { "term": { "user.id": "{{user_id}}" }}]}}}',
        params: {
          year_scope: true,
          user_id: 'kimchy'
        }
      }
    )
    puts response
    
    
    POST _render/template
    {
      "source": "{ \"query\": { \"bool\": { \"filter\": [ {{#year_scope}} { \"range\": { \"@timestamp\": { \"gte\": \"now-1y/d\", \"lt\": \"now/d\" } } }, {{/year_scope}} { \"term\": { \"user.id\": \"{{user_id}}\" }}]}}}",
      "params": {
        "year_scope": true,
        "user_id": "kimchy"
      }
    }

模板呈现为：

    
    
    {
      "template_output" : {
        "query" : {
          "bool" : {
            "filter" : [
              {
                "range" : {
                  "@timestamp" : {
                    "gte" : "now-1y/d",
                    "lt" : "now/d"
                  }
                }
              },
              {
                "term" : {
                  "user.id" : "kimchy"
                }
              }
            ]
          }
        }
      }
    }

如果"year_scope"为"false"，则模板将搜索任何时间段的数据。

    
    
    response = client.render_search_template(
      body: {
        source: '{ "query": { "bool": { "filter": [ {{#year_scope}} { "range": { "@timestamp": { "gte": "now-1y/d", "lt": "now/d" } } }, {{/year_scope}} { "term": { "user.id": "{{user_id}}" }}]}}}',
        params: {
          year_scope: false,
          user_id: 'kimchy'
        }
      }
    )
    puts response
    
    
    POST _render/template
    {
      "source": "{ \"query\": { \"bool\": { \"filter\": [ {{#year_scope}} { \"range\": { \"@timestamp\": { \"gte\": \"now-1y/d\", \"lt\": \"now/d\" } } }, {{/year_scope}} { \"term\": { \"user.id\": \"{{user_id}}\" }}]}}}",
      "params": {
        "year_scope": false,
        "user_id": "kimchy"
      }
    }

模板呈现为：

    
    
    {
      "template_output" : {
        "query" : {
          "bool" : {
            "filter" : [
              {
                "term" : {
                  "user.id" : "kimchy"
                }
              }
            ]
          }
        }
      }
    }

若要创建 if-else 条件，请使用以下语法：

    
    
    {{#condition}}if content{{/condition}} {{^condition}}else content{{/condition}}

例如，如果"year_scope"为"true"，则以下模板搜索过去一年的数据。否则，它将搜索过去一天的数据。

    
    
    response = client.render_search_template(
      body: {
        source: '{ "query": { "bool": { "filter": [ { "range": { "@timestamp": { "gte": {{#year_scope}} "now-1y/d" {{/year_scope}} {{^year_scope}} "now-1d/d" {{/year_scope}} , "lt": "now/d" }}}, { "term": { "user.id": "{{user_id}}" }}]}}}',
        params: {
          year_scope: true,
          user_id: 'kimchy'
        }
      }
    )
    puts response
    
    
    POST _render/template
    {
      "source": "{ \"query\": { \"bool\": { \"filter\": [ { \"range\": { \"@timestamp\": { \"gte\": {{#year_scope}} \"now-1y/d\" {{/year_scope}} {{^year_scope}} \"now-1d/d\" {{/year_scope}} , \"lt\": \"now/d\" }}}, { \"term\": { \"user.id\": \"{{user_id}}\" }}]}}}",
      "params": {
        "year_scope": true,
        "user_id": "kimchy"
      }
    }

[« Search shard routing](search-shard-routing.md) [Search template examples
with Mustache »](search-template-with-mustache-examples.md)

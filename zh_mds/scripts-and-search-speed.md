

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Scripting](modules-scripting.md) ›[How to write scripts](modules-
scripting-using.md)

[« How to write scripts](modules-scripting-using.md) [Dissecting data
»](dissect.md)

## 脚本、缓存和搜索速度

Elasticsearch 执行了许多优化，以尽可能快地使用脚本。一个重要的优化是脚本缓存。编译的脚本放置在缓存中，以便引用脚本的请求不会产生编译损失。

缓存大小调整很重要。脚本缓存应足够大，以容纳用户需要并发访问的所有脚本。

如果您在节点统计信息中看到大量脚本缓存逐出和越来越多的编译，则您的缓存可能太小。

默认情况下，所有脚本都缓存，因此只需在发生更新时重新编译它们。默认情况下，脚本没有基于时间的过期时间。您可以使用"script.cache.expire"设置更改此行为。使用"script.cache.max_size"设置来配置缓存的大小。

脚本的大小限制为 65，535 字节。设置"script.max_size_in_bytes"的值以增加该软限制。如果您的脚本非常大，请考虑使用本机脚本引擎。

#### 提高搜索速度

脚本非常有用，但不能使用 Elasticsearch 的索引结构或相关的优化。这种关系有时会导致搜索速度变慢。

如果您经常使用脚本来转换索引数据，则可以通过在引入期间转换数据来加快搜索速度。但是，这通常意味着较慢的索引速度。让我们看一个实际示例来说明如何提高搜索速度。

运行搜索时，通常按两个值的总和对结果进行排序。例如，考虑一个名为"my_test_scores"的索引，其中包含测试分数数据。此索引包括两个类型为"long"的字段：

* "math_score" * "verbal_score"

您可以使用将这些值相加的脚本运行查询。这种方法没有错，但查询会变慢，因为脚本评估是作为请求的一部分发生的。以下请求返回"grad_year"等于"2099"的文档，并按脚本的升值结果排序。

    
    
    response = client.search(
      index: 'my_test_scores',
      body: {
        query: {
          term: {
            grad_year: '2099'
          }
        },
        sort: [
          {
            _script: {
              type: 'number',
              script: {
                source: "doc['math_score'].value + doc['verbal_score'].value"
              },
              order: 'desc'
            }
          }
        ]
      }
    )
    puts response
    
    
    GET /my_test_scores/_search
    {
      "query": {
        "term": {
          "grad_year": "2099"
        }
      },
      "sort": [
        {
          "_script": {
            "type": "number",
            "script": {
              "source": "doc['math_score'].value + doc['verbal_score'].value"
            },
            "order": "desc"
          }
        }
      ]
    }

如果要搜索小型索引，则将脚本作为搜索查询的一部分包含在内可能是一个很好的解决方案。如果要加快搜索速度，可以在引入期间执行此计算，并将总和索引到字段。

首先，我们将向索引添加一个名为"total_score"的新字段，该字段将包含"math_score"和"verbal_score"字段值的总和。

    
    
    response = client.indices.put_mapping(
      index: 'my_test_scores',
      body: {
        properties: {
          total_score: {
            type: 'long'
          }
        }
      }
    )
    puts response
    
    
    PUT /my_test_scores/_mapping
    {
      "properties": {
        "total_score": {
          "type": "long"
        }
      }
    }

接下来，使用包含脚本处理器的摄取管道来计算"math_score"和"verbal_score"的总和，并在"total_score"字段中对其进行索引。

    
    
    response = client.ingest.put_pipeline(
      id: 'my_test_scores_pipeline',
      body: {
        description: 'Calculates the total test score',
        processors: [
          {
            script: {
              source: 'ctx.total_score = (ctx.math_score + ctx.verbal_score)'
            }
          }
        ]
      }
    )
    puts response
    
    
    PUT _ingest/pipeline/my_test_scores_pipeline
    {
      "description": "Calculates the total test score",
      "processors": [
        {
          "script": {
            "source": "ctx.total_score = (ctx.math_score + ctx.verbal_score)"
          }
        }
      ]
    }

若要更新现有数据，请使用此管道将任何文档从"my_test_scores"重新索引到名为"my_test_scores_2"的新索引。

    
    
    response = client.reindex(
      body: {
        source: {
          index: 'my_test_scores'
        },
        dest: {
          index: 'my_test_scores_2',
          pipeline: 'my_test_scores_pipeline'
        }
      }
    )
    puts response
    
    
    POST /_reindex
    {
      "source": {
        "index": "my_test_scores"
      },
      "dest": {
        "index": "my_test_scores_2",
        "pipeline": "my_test_scores_pipeline"
      }
    }

继续使用管道将任何新文档索引为"my_test_scores_2"。

    
    
    POST /my_test_scores_2/_doc/?pipeline=my_test_scores_pipeline
    {
      "student": "kimchy",
      "grad_year": "2099",
      "math_score": 1200,
      "verbal_score": 800
    }

这些更改会减慢索引过程，但允许更快的搜索。您可以使用"total_score"字段对在"my_test_scores_2"上进行的搜索进行排序，而不是使用脚本。响应近乎实时！虽然这个过程最慢的时间，但它大大增加了搜索时的查询。

    
    
    response = client.search(
      index: 'my_test_scores_2',
      body: {
        query: {
          term: {
            grad_year: '2099'
          }
        },
        sort: [
          {
            total_score: {
              order: 'desc'
            }
          }
        ]
      }
    )
    puts response
    
    
    GET /my_test_scores_2/_search
    {
      "query": {
        "term": {
          "grad_year": "2099"
        }
      },
      "sort": [
        {
          "total_score": {
            "order": "desc"
          }
        }
      ]
    }

[« How to write scripts](modules-scripting-using.md) [Dissecting data
»](dissect.md)



[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[How
to](how-to.md) ›[Recipes](recipes.md)

[« Getting consistent scoring](consistent-scoring.md) [Tune for indexing
speed »](tune-for-indexing-speed.md)

## 将静态相关性信号合并到分数中

许多域具有已知与相关性相关的静态信号。例如，PageRank和url长度是Web搜索的两个常用功能，以便独立于查询来调整网页的分数。

有两个主要查询允许将静态分数贡献与文本相关性相结合，例如。使用 BM25 计算：\- 'script_score'查询 \-'rank_feature' 查询

例如，假设您有一个"pagerank"字段，您希望将其与BM25分数相结合，以便最终分数等于"score = bm25_score +pagerank / (10 + pagerank)"。

使用"script_score"查询，查询将如下所示：

    
    
    response = client.search(
      index: 'index',
      body: {
        query: {
          script_score: {
            query: {
              match: {
                body: 'elasticsearch'
              }
            },
            script: {
              source: "_score * saturation(doc['pagerank'].value, 10)"
            }
          }
        }
      }
    )
    puts response
    
    
    GET index/_search
    {
      "query": {
        "script_score": {
          "query": {
            "match": { "body": "elasticsearch" }
          },
          "script": {
            "source": "_score * saturation(doc['pagerank'].value, 10)" __}
        }
      }
    }

__

|

"pagerank"必须映射为数字---|---而使用"rank_feature"查询时，它如下所示：

    
    
    response = client.search(
      body: {
        query: {
          bool: {
            must: {
              match: {
                body: 'elasticsearch'
              }
            },
            should: {
              rank_feature: {
                field: 'pagerank',
                saturation: {
                  pivot: 10
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET _search
    {
      "query": {
        "bool": {
          "must": {
            "match": { "body": "elasticsearch" }
          },
          "should": {
            "rank_feature": {
              "field": "pagerank", __"saturation": {
                "pivot": 10
              }
            }
          }
        }
      }
    }

__

|

"PageRank"必须映射为"rank_feature"字段---|--- 虽然这两个选项都会返回相似的分数，但也有权衡：script_scoreprovides很大的灵活性，使您能够根据需要将文本相关性分数与静态信号相结合。另一方面，"rank_feature"查询仅公开了几种将静态信号合并到分数中的方法。但是，它依赖于"rank_feature"和"rank_features"字段，这些字段以特殊方式索引值，允许"rank_feature"查询跳过过度竞争的文档并更快地获得查询的顶级匹配项。

[« Getting consistent scoring](consistent-scoring.md) [Tune for indexing
speed »](tune-for-indexing-speed.md)

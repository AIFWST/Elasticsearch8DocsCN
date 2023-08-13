

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Metrics aggregations](search-
aggregations-metrics.md)

[« Sum aggregation](search-aggregations-metrics-sum-aggregation.md) [Top
hits aggregation »](search-aggregations-metrics-top-hits-aggregation.md)

## T 测试聚合

执行统计假设检验的"t_test"指标聚合，其中检验统计量遵循从聚合文档中提取的数值的原假设下的学生 t 分布。在实践中，这将告诉您两个总体均值之间的差异是否具有统计显著性，并且不是偶然发生的。

###Syntax

"t_test"聚合单独如下所示：

    
    
    {
      "t_test": {
        "a": "value_before",
        "b": "value_after",
        "type": "paired"
      }
    }

假设我们有升级前后节点启动时间的记录，让我们看一个 t 检验，看看升级是否以有意义的方式影响了节点启动正常运行时间。

    
    
    response = client.search(
      index: 'node_upgrade',
      body: {
        size: 0,
        aggregations: {
          startup_time_ttest: {
            t_test: {
              a: {
                field: 'startup_time_before'
              },
              b: {
                field: 'startup_time_after'
              },
              type: 'paired'
            }
          }
        }
      }
    )
    puts response
    
    
    GET node_upgrade/_search
    {
      "size": 0,
      "aggs": {
        "startup_time_ttest": {
          "t_test": {
            "a": { "field": "startup_time_before" },  __"b": { "field": "startup_time_after" }, __"type": "paired" __}
        }
      }
    }

__

|

字段"startup_time_before"必须是数值字段。   ---|---    __

|

字段"startup_time_after"必须是数值字段。   __

|

由于我们有来自相同节点的数据，因此我们使用配对 t 检验。   响应将返回检验的 p 值或概率值。它是获得结果的概率，至少与聚合处理的结果一样极端，假设原假设是正确的(这意味着总体均值之间没有差异)。较小的 p 值意味着原假设更有可能不正确，总体均值确实不同。

    
    
    {
      ...
    
     "aggregations": {
        "startup_time_ttest": {
          "value": 0.1914368843365979 __}
      }
    }

__

|

p 值。   ---|--- ### T-测试类型编辑

"t_test"聚合支持未配对和配对的双样本 t 检验。可以使用"type"参数指定测试的类型：

"类型"： "配对"'

     performs paired t-test 
`"type": "homoscedastic"`

     performs two-sample equal variance test 
`"type": "heteroscedastic"`

     performs two-sample unequal variance test (this is default) 

###Filters

也可以使用过滤器对不同的记录集运行非配对 t 检验。例如，如果我们想测试两个不同节点组之间升级前启动时间的差异，我们将在组名称字段上使用术语过滤器的单独节点组使用相同的字段"startup_time_before"：

    
    
    response = client.search(
      index: 'node_upgrade',
      body: {
        size: 0,
        aggregations: {
          startup_time_ttest: {
            t_test: {
              a: {
                field: 'startup_time_before',
                filter: {
                  term: {
                    group: 'A'
                  }
                }
              },
              b: {
                field: 'startup_time_before',
                filter: {
                  term: {
                    group: 'B'
                  }
                }
              },
              type: 'heteroscedastic'
            }
          }
        }
      }
    )
    puts response
    
    
    GET node_upgrade/_search
    {
      "size": 0,
      "aggs": {
        "startup_time_ttest": {
          "t_test": {
            "a": {
              "field": "startup_time_before",         __"filter": {
                "term": {
                  "group": "A" __}
              }
            },
            "b": {
              "field": "startup_time_before", __"filter": {
                "term": {
                  "group": "B" __}
              }
            },
            "type": "heteroscedastic" __}
        }
      }
    }

__

|

字段"startup_time_before"必须是数值字段。   ---|---    __

|

可以在此处使用分隔两个组的任何查询。   __

|

我们使用相同的字段 __

|

但是我们使用不同的过滤器。   __

|

由于我们有来自不同节点的数据，所以我们不能使用配对 t 检验。               {      ...        "聚合"： { "startup_time_ttest"： { "值"： 0.2981858007281437 __} } }

__

|

p 值。   ---|--- 总体不必在同一索引中。如果数据集位于不同的索引中，则可以使用"_index"字段中的术语过滤器来选择总体。

###Script

如果需要对未由 afield 明确表示的值运行"t_test"，请在运行时字段上运行聚合。例如，如果要调整之前值的加载时间：

    
    
    response = client.search(
      index: 'node_upgrade',
      body: {
        size: 0,
        runtime_mappings: {
          "startup_time_before.adjusted": {
            type: 'long',
            script: {
              source: "emit(doc['startup_time_before'].value - params.adjustment)",
              params: {
                adjustment: 10
              }
            }
          }
        },
        aggregations: {
          startup_time_ttest: {
            t_test: {
              a: {
                field: 'startup_time_before.adjusted'
              },
              b: {
                field: 'startup_time_after'
              },
              type: 'paired'
            }
          }
        }
      }
    )
    puts response
    
    
    GET node_upgrade/_search
    {
      "size": 0,
      "runtime_mappings": {
        "startup_time_before.adjusted": {
          "type": "long",
          "script": {
            "source": "emit(doc['startup_time_before'].value - params.adjustment)",
            "params": {
              "adjustment": 10
            }
          }
        }
      },
      "aggs": {
        "startup_time_ttest": {
          "t_test": {
            "a": {
              "field": "startup_time_before.adjusted"
            },
            "b": {
              "field": "startup_time_after"
            },
            "type": "paired"
          }
        }
      }
    }

[« Sum aggregation](search-aggregations-metrics-sum-aggregation.md) [Top
hits aggregation »](search-aggregations-metrics-top-hits-aggregation.md)

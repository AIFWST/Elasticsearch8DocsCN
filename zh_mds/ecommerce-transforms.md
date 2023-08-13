

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Roll up or
transform your data](data-rollup-transform.md) ›[Transforming
data](transforms.md)

[« API quick reference](transform-api-quickref.md) [Transform examples
»](transform-examples.md)

## 教程：转换电子商务示例数据

转换使您能够从 Elasticsearch 索引中检索信息，对其进行转换，并将其存储在另一个索引中。让我们使用 Kibana 示例数据来演示如何使用转换透视和汇总数据。

1. 验证您的环境是否已正确设置为使用转换。如果启用了 Elasticsearch 安全功能，要完成本教程，您需要一个有权预览和创建转换的用户。您还必须具有源索引和目标索引的特定索引特权。请参阅设置。  2. 选择您的_source index_。

在此示例中，我们将使用电子商务订单示例数据。如果您还不熟悉"kibana_sample_data_ecommerce"指数，请使用 Kibana 中的"收入"控制面板浏览数据。考虑您可能希望从此电子商务数据中获得哪些见解。

3. 选择转换的透视类型，并使用各种选项对数据进行分组和聚合。

有两种类型的转换，但首先我们将尝试 _pivoting_ yourdata，这涉及使用至少一个字段对其进行分组并应用至少一个聚合。您可以预览转换后的数据的外观，因此请继续使用它！您还可以启用直方图以更好地了解数据中值的分布。

例如，您可能希望按产品 ID 对数据进行分组，并计算每个产品的总销售额及其平均价格。或者，您可能希望查看单个客户的行为，并计算每个客户总共花费了多少以及他们购买了多少不同类别的产品。或者，您可能需要考虑货币或地理位置。转换和解释这些数据的最有趣的方法是什么？

在 Kibana 中转到 **管理** > **堆栈管理** > **数据** > **转换**，然后使用向导创建转换：

!在 Kibana 中创建简单的变换

按客户 ID 对数据进行分组，并添加一个或多个聚合以了解有关每个客户订单的详细信息。例如，让我们计算他们购买的产品总和、购买的总价、他们在单个订单中购买的最大产品数量以及他们的订单总数。我们将通过在"total_quantity"和"taxless_total_price"字段上使用"sum"聚合、在"total_quantity"字段上使用"max"聚合以及"order_id"字段上的"基数"聚合来实现这一点：

!在 Kibana 中向转换添加多个聚合

如果对数据的子集感兴趣，可以选择包含查询元素。在此示例中，我们筛选了数据，以便仅查看"货币"为"EUR"的订单。或者，我们也可以按该字段对数据进行分组。如果要使用更复杂的查询，可以通过保存的搜索创建数据框。

如果愿意，可以使用预览转换 API。

接口示例

    
        POST _transform/_preview
    {
      "source": {
        "index": "kibana_sample_data_ecommerce",
        "query": {
          "bool": {
            "filter": {
              "term": {"currency": "EUR"}
            }
          }
        }
      },
      "pivot": {
        "group_by": {
          "customer_id": {
            "terms": {
              "field": "customer_id"
            }
          }
        },
        "aggregations": {
          "total_quantity.sum": {
            "sum": {
              "field": "total_quantity"
            }
          },
          "taxless_total_price.sum": {
            "sum": {
              "field": "taxless_total_price"
            }
          },
          "total_quantity.max": {
            "max": {
              "field": "total_quantity"
            }
          },
          "order_id.cardinality": {
            "cardinality": {
              "field": "order_id"
            }
          }
        }
      }
    }

4. 如果您对预览中看到的内容感到满意，请创建转换。

    1. Supply a transform ID, the name of the destination index and optionally a description. If the destination index does not exist, it will be created automatically when you start the transform. 
    2. Decide whether you want the transform to run once or continuously. Since this sample data index is unchanging, let's use the default behavior and just run the transform once. If you want to try it out, however, go ahead and click on **Continuous mode**. You must choose a field that the transform can use to check which entities have changed. In general, it's a good idea to use the ingest timestamp field. In this example, however, you can use the `order_date` field. 
    3. Optionally, you can configure a retention policy that applies to your transform. Select a date field that is used to identify old documents in the destination index and provide a maximum age. Documents that are older than the configured value are removed from the destination index. 

!将转换自 ID 和保留策略添加到转换 InKibana

在 Kibana 中，在完成转换创建之前，可以将预览转换 API 请求复制到剪贴板。稍后决定是否要手动创建目标索引时，此信息非常有用。

!将转换预览的开发控制台语句复制到剪贴板

如果您愿意，可以使用创建转换 API。

接口示例

    
        PUT _transform/ecommerce-customer-transform
    {
      "source": {
        "index": [
          "kibana_sample_data_ecommerce"
        ],
        "query": {
          "bool": {
            "filter": {
              "term": {
                "currency": "EUR"
              }
            }
          }
        }
      },
      "pivot": {
        "group_by": {
          "customer_id": {
            "terms": {
              "field": "customer_id"
            }
          }
        },
        "aggregations": {
          "total_quantity.sum": {
            "sum": {
              "field": "total_quantity"
            }
          },
          "taxless_total_price.sum": {
            "sum": {
              "field": "taxless_total_price"
            }
          },
          "total_quantity.max": {
            "max": {
              "field": "total_quantity"
            }
          },
          "order_id.cardinality": {
            "cardinality": {
              "field": "order_id"
            }
          }
        }
      },
      "dest": {
        "index": "ecommerce-customers"
      },
      "retention_policy": {
        "time": {
          "field": "order_date",
          "max_age": "60d"
        }
      }
    }

5. 可选：创建目标索引。

如果目标索引不存在，则会在首次启动转换时创建该索引。透视转换从源索引和转换聚合中推断目标索引的映射。如果目标索引中存在派生自脚本的字段(例如，如果使用"scripted_metrics"或"bucket_scripts"聚合)，则会使用动态映射创建这些字段。可以使用预览转换 API 预览它将用于目标索引的映射。在 Kibana 中，如果您将 API 请求复制到剪贴板，请将其粘贴到控制台中，然后在 API 响应中引用"generated_dest_index"对象。

与 Kibana 中提供的选项相比，转换可能具有更多 API 提供的配置选项。例如，可以通过调用"创建"转换来为"dest"设置引入管道。有关所有转换配置选项，请参阅文档。

接口示例

    
        {
      "preview" : [
        {
          "total_quantity" : {
            "max" : 2,
            "sum" : 118.0
          },
          "taxless_total_price" : {
            "sum" : 3946.9765625
          },
          "customer_id" : "10",
          "order_id" : {
            "cardinality" : 59
          }
        },
        ...
      ],
      "generated_dest_index" : {
        "mappings" : {
          "_meta" : {
            "_transform" : {
              "transform" : "transform-preview",
              "version" : {
                "created" : "8.0.0"
              },
              "creation_date_in_millis" : 1621991264061
            },
            "created_by" : "transform"
          },
          "properties" : {
            "total_quantity.sum" : {
              "type" : "double"
            },
            "total_quantity" : {
              "type" : "object"
            },
            "taxless_total_price" : {
              "type" : "object"
            },
            "taxless_total_price.sum" : {
              "type" : "double"
            },
            "order_id.cardinality" : {
              "type" : "long"
            },
            "customer_id" : {
              "type" : "keyword"
            },
            "total_quantity.max" : {
              "type" : "integer"
            },
            "order_id" : {
              "type" : "object"
            }
          }
        },
        "settings" : {
          "index" : {
            "number_of_shards" : "1",
            "auto_expand_replicas" : "0-1"
          }
        },
        "aliases" : { }
      }
    }

在某些情况下，推导的映射可能与实际数据不兼容。例如，可能会发生数字溢出，或者动态映射的字段可能包含数字和字符串。若要避免此问题，请在开始转换之前创建目标索引。有关详细信息，请参阅创建索引 API。

接口示例

可以使用转换预览中的信息来创建目标索引。例如：

    
        response = client.indices.create(
      index: 'ecommerce-customers',
      body: {
        mappings: {
          properties: {
            "total_quantity.sum": {
              type: 'double'
            },
            total_quantity: {
              type: 'object'
            },
            taxless_total_price: {
              type: 'object'
            },
            "taxless_total_price.sum": {
              type: 'double'
            },
            "order_id.cardinality": {
              type: 'long'
            },
            customer_id: {
              type: 'keyword'
            },
            "total_quantity.max": {
              type: 'integer'
            },
            order_id: {
              type: 'object'
            }
          }
        }
      }
    )
    puts response
    
        PUT /ecommerce-customers
    {
      "mappings": {
        "properties": {
          "total_quantity.sum" : {
            "type" : "double"
          },
          "total_quantity" : {
            "type" : "object"
          },
          "taxless_total_price" : {
            "type" : "object"
          },
          "taxless_total_price.sum" : {
            "type" : "double"
          },
          "order_id.cardinality" : {
            "type" : "long"
          },
          "customer_id" : {
            "type" : "keyword"
          },
          "total_quantity.max" : {
            "type" : "integer"
          },
          "order_id" : {
            "type" : "object"
          }
        }
      }
    }

6. 开始转换。

即使资源利用率会根据群集负载自动调整，转换也会在群集运行时增加群集上的搜索和索引负载。但是，如果您遇到负载过大，则可以停止它。

您可以在 Kibana 中启动、停止、重置和管理转换：

!在 Kibana 中管理转换

或者，可以使用启动转换、停止转换和重置转换 API。

如果重置转换，则会删除所有检查点、状态和目标索引(如果它是由转换创建的)。转换已准备好再次启动，就像刚刚创建一样。

接口示例

    
        response = client.transform.start_transform(
      transform_id: 'ecommerce-customer-transform'
    )
    puts response
    
        POST _transform/ecommerce-customer-transform/_start

如果选择批量转换，则它是具有单个检查点的单个操作。完成后无法重新启动它。连续转换的不同之处在于，它们在引入新源数据时不断递增和处理检查点。

7. 浏览新索引中的数据。

例如，在 Kibana 中使用 **发现** 应用程序：

!探索 Kibana 中的新索引

8. 可选：创建另一个转换，这次使用"最新"方法。

此方法使用每个唯一键值的最新文档填充目标索引。例如，您可能希望查找每个客户或每个国家和地区的最新订单(按"order_date"字段排序)。

!在 Kibana 中创建最新变换

接口示例

    
        POST _transform/_preview
    {
      "source": {
        "index": "kibana_sample_data_ecommerce",
        "query": {
          "bool": {
            "filter": {
              "term": {"currency": "EUR"}
            }
          }
        }
      },
      "latest": {
        "unique_key": ["geoip.country_iso_code", "geoip.region_name"],
        "sort": "order_date"
      }
    }

如果目标索引不存在，则会在首次启动转换时创建该索引。但是，与透视转换不同，最新转换在创建索引时不会推断映射定义。相反，它们使用动态映射。若要使用显式映射，请在开始转换之前创建目标索引。

9. 如果您不想保留转换，可以在 Kibana 中删除它或使用删除转换 API。默认情况下，删除转换时，其目标索引和 Kibana 索引模式将保留。

现在，您已经为 Kibana 示例数据创建了简单的转换，接下来可以为您自己的数据考虑一些可能的用例。有关更多想法，请参阅何时使用转换和示例。

[« API quick reference](transform-api-quickref.md) [Transform examples
»](transform-examples.md)

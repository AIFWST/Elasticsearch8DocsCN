

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Search your
data](search-your-data.md)

[« Retrieve selected fields from a search](search-fields.md) [Search
multiple data streams and indices »](search-multiple-indices.md)

## 跨集群搜索

跨集群搜索允许您对一个或多个远程集群运行单个搜索请求。例如，您可以使用跨集群搜索来筛选和分析存储在不同数据中心的集群上的日志数据。

### 支持的接口

以下 API 支持跨集群搜索：

* 搜索 * 异步搜索 * 多重搜索 * 搜索模板 * 多搜索模板 * 字段功能 * 无痛执行 API * 预览] 此功能处于技术预览状态，可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持约束。 [EQL 搜索 * 预览] 此功能处于技术预览阶段，可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持约束。 [SQL 搜索 * 预览] 此功能处于技术预览阶段，可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持约束。 [矢量图块搜索

###Prerequisites

* 跨集群搜索需要远程集群。要在 Elasticsearch Service 上设置远程集群，请参见在 Elasticsearch Service 上配置远程集群。如果您在自己的硬件上运行 Elasticsearch，请参阅_Remote clusters_。

要确保您的远程集群配置支持跨集群搜索，请参阅支持的跨集群搜索配置。

* 对于完整的跨群集搜索功能，本地和远程群集必须位于同一订阅级别。  * 本地协调节点必须具有"remote_cluster_client"节点角色。

* 如果使用嗅探模式，则本地协调节点必须能够连接到远程群集上的种子节点和网关节点。

我们建议使用能够充当协调节点的网关节点。这些节点可以是这些网关节点的子集。

* 如果使用代理模式，则本地协调节点必须能够连接到配置的"proxy_address"。此地址的代理必须能够将连接路由到远程群集上的网关和协调节点。  * 跨集群搜索需要对本地集群和远程集群具有不同的安全权限。请参阅配置跨集群搜索的权限和配置跨集群搜索和 Kibana 的权限。

### 跨集群搜索示例

#### 远程群集设置

以下群集更新设置 API 请求添加三个远程群集："cluster_one"、"cluster_two"和"cluster_three"。

    
    
    PUT _cluster/settings
    {
      "persistent": {
        "cluster": {
          "remote": {
            "cluster_one": {
              "seeds": [
                "127.0.0.1:9300"
              ]
            },
            "cluster_two": {
              "seeds": [
                "127.0.0.1:9301"
              ]
            },
            "cluster_three": {
              "seeds": [
                "127.0.0.1:9302"
              ]
            }
          }
        }
      }
    }

#### 搜索单个远程群集

在搜索请求中，您将远程群集上的数据流和索引指定为"<remote_cluster_name>："<target>。

以下搜索 API 请求搜索单个远程群集"cluster_one"上的"my-index-000001"索引。

    
    
    response = client.search(
      index: 'cluster_one:my-index-000001',
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        },
        _source: [
          'user.id',
          'message',
          'http.response.status_code'
        ]
      }
    )
    puts response
    
    
    GET /cluster_one:my-index-000001/_search
    {
      "query": {
        "match": {
          "user.id": "kimchy"
        }
      },
      "_source": ["user.id", "message", "http.response.status_code"]
    }

API 返回以下响应：

    
    
    {
      "took": 150,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "failed": 0,
        "skipped": 0
      },
      "_clusters": {
        "total": 1,
        "successful": 1,
        "skipped": 0
      },
      "hits": {
        "total" : {
            "value": 1,
            "relation": "eq"
        },
        "max_score": 1,
        "hits": [
          {
            "_index": "cluster_one:my-index-000001", __"_id": "0",
            "_score": 1,
            "_source": {
              "user": {
                "id": "kimchy"
              },
              "message": "GET /search HTTP/1.1 200 1070000",
              "http": {
                "response":
                  {
                    "status_code": 200
                  }
              }
            }
          }
        ]
      }
    }

__

|

搜索响应正文在"_index"参数中包含远程群集的名称。   ---|--- #### 搜索多个远程群集编辑

以下搜索 API 请求在三个集群上搜索"my-index-000001"索引：

* 您的本地集群 * 两个远程集群，"cluster_one"和"cluster_two"

    
    
    response = client.search(
      index: 'my-index-000001,cluster_one:my-index-000001,cluster_two:my-index-000001',
      body: {
        query: {
          match: {
            "user.id": 'kimchy'
          }
        },
        _source: [
          'user.id',
          'message',
          'http.response.status_code'
        ]
      }
    )
    puts response
    
    
    GET /my-index-000001,cluster_one:my-index-000001,cluster_two:my-index-000001/_search
    {
      "query": {
        "match": {
          "user.id": "kimchy"
        }
      },
      "_source": ["user.id", "message", "http.response.status_code"]
    }

API 返回以下响应：

    
    
    {
      "took": 150,
      "timed_out": false,
      "num_reduce_phases": 4,
      "_shards": {
        "total": 3,
        "successful": 3,
        "failed": 0,
        "skipped": 0
      },
      "_clusters": {
        "total": 3,
        "successful": 3,
        "skipped": 0
      },
      "hits": {
        "total" : {
            "value": 3,
            "relation": "eq"
        },
        "max_score": 1,
        "hits": [
          {
            "_index": "my-index-000001", __"_id": "0",
            "_score": 2,
            "_source": {
              "user": {
                "id": "kimchy"
              },
              "message": "GET /search HTTP/1.1 200 1070000",
              "http": {
                "response":
                  {
                    "status_code": 200
                  }
              }
            }
          },
          {
            "_index": "cluster_one:my-index-000001", __"_id": "0",
            "_score": 1,
            "_source": {
              "user": {
                "id": "kimchy"
              },
              "message": "GET /search HTTP/1.1 200 1070000",
              "http": {
                "response":
                  {
                    "status_code": 200
                  }
              }
            }
          },
          {
            "_index": "cluster_two:my-index-000001", __"_id": "0",
            "_score": 1,
            "_source": {
              "user": {
                "id": "kimchy"
              },
              "message": "GET /search HTTP/1.1 200 1070000",
              "http": {
                "response":
                  {
                    "status_code": 200
                  }
              }
            }
          }
        ]
      }
    }

__

|

本文档的"_index"参数不包含群集名称。这意味着文档来自本地群集。   ---|---    __

|

该文件来自"cluster_one"。   __

|

此文档来自"cluster_two"。   ### 使用异步搜索进行跨集群搜索 withccs_minimize_roundtrips=trueedit

可以使用异步搜索 API 异步查询远程群集。异步搜索接受默认为"false"的"ccs_minimize_roundtrips"参数。请参阅最小化网络往返以了解有关此选项的详细信息。

以下请求使用"ccs_minimize_roundtrips=true"对三个集群异步搜索"my-index-000001"索引：

* 本地集群，有 8 个分片 * 两个远程集群，"cluster_one"和"cluster_two"，每个集群有 10 个分片

    
    
    POST /my-index-000001,cluster_one:my-index-000001,cluster_two:my-index-000001/_async_search?ccs_minimize_roundtrips=true
    {
      "query": {
        "match": {
          "user.id": "kimchy"
        }
      },
      "_source": ["user.id", "message", "http.response.status_code"]
    }

API 返回以下响应：

    
    
    {
      "id": "FklQYndoTDJ2VEFlMEVBTzFJMGhJVFEaLVlKYndBWWZSMUdicUc4WVlEaFl4ZzoxNTU=", __"is_partial": true,
      "is_running": true,
      "start_time_in_millis": 1685563581380,
      "expiration_time_in_millis": 1685995581380,
      "response": {
        "took": 1020,
        "timed_out": false,
        "num_reduce_phases": 0,
        "_shards": {
          "total": 8, __"successful": 0,
          "failed": 0,
          "skipped": 0
        },
        "_clusters": { __"total" : 3,
          "successful" : 0,
          "skipped": 0
        },
        "hits": {
          "total" : {
              "value": 0,
              "relation": "eq"
          },
          "max_score": null,
          "hits": []
        }
      }
    }

__

|

异步搜索 ID。   ---|---    __

|

当"ccs_minimize_roundtrips"="true"并且远程集群上的搜索仍在运行时，此部分仅指示本地集群范围内的分片数。仅当搜索完成时，才会更新此分片数以包括所有集群中的分片总数。   __

|

"_clusters"部分表示 3 个集群在搜索范围内，并且所有集群当前都在运行(因为"成功"和"跳过"都等于 0)。   如果在查询仍在运行时查询 get 异步搜索终结点，则在本地搜索完成后，将在响应的"_clusters"和"_shards"部分看到更新。

    
    
    GET /_async_search/FklQYndoTDJ2VEFlMEVBTzFJMGhJVFEaLVlKYndBWWZSMUdicUc4WVlEaFl4ZzoxNTU=

Response:

    
    
    {
      "id": "FklQYndoTDJ2VEFlMEVBTzFJMGhJVFEaLVlKYndBWWZSMUdicUc4WVlEaFl4ZzoxNTU=",
      "is_partial": true,
      "is_running": true,
      "start_time_in_millis": 1685564911108,
      "expiration_time_in_millis": 1685996911108,
      "response": {
        "took": 11164,
        "timed_out": false,
        "terminated_early": false,
        "_shards": {
          "total": 8,
          "successful": 8,  __"skipped": 0,
          "failed": 0
        },
        "_clusters": {
          "total": 3,
          "successful": 1, __"skipped": 0
        },
        "hits": {
          "total": {
            "value": 167, __"relation": "eq"
          },
          "max_score": null,
          "hits": []
        }
      }
    }

__

|

所有本地集群分片均已完成。   ---|---    __

|

本地群集搜索已完成，因此"成功"群集条目设置为 1。在所有远程搜索完成(成功或跳过)之前，不会更新远程群集的"_clusters"响应部分。   __

|

来自本地群集搜索的命中数。在完成并合并所有群集的搜索之前，不会显示最终命中。   完成对所有集群的搜索后，当您查询 getasync 搜索终端节点时，您将看到"_clusters"和"_shards"部分的最终状态以及命中数。

    
    
    GET /_async_search/FklQYndoTDJ2VEFlMEVBTzFJMGhJVFEaLVlKYndBWWZSMUdicUc4WVlEaFl4ZzoxNTU=

Response:

    
    
    {
      "id": "FklQYndoTDJ2VEFlMEVBTzFJMGhJVFEaLVlKYndBWWZSMUdicUc4WVlEaFl4ZzoxNTU=",
      "is_partial": false,
      "is_running": false,
      "start_time_in_millis": 1685564911108,
      "expiration_time_in_millis": 1685996911108,
      "response": {
        "took": 27619,
        "timed_out": false,
        "num_reduce_phases": 4,
        "_shards": {
          "total": 28,
          "successful": 28,  __"skipped": 0,
          "failed": 0
        },
        "_clusters": {
          "total": 3,
          "successful": 3, __"skipped": 0
        },
        "hits": {
          "total": {
            "value": 1067,
            "relation": "eq"
          },
          "max_score": 1.8293576,
          "hits": [...list of hits here...]
        }
      }
    }

__

|

"_shards"部分现已更新，以显示我们在所有集群中总共研究了 28 个分片，并且所有分片都取得了成功。   ---|---    __

|

"_clusters"部分显示对所有 3 个集群的搜索都成功。   ### 使用异步搜索进行跨集群搜索 withccs_minimize_roundtrips=falseedit

当异步搜索中的"ccs_minimize_roundtrips"为"false"时，响应的"_shards"和"_clusters"部分的行为会有所不同。

主要区别在于：

1. "_shards"部分的总数将立即准确，因为在搜索开始之前从所有集群中收集了分片总数。  2. "_shards"部分将随着对单个分片的搜索完成而逐步更新，因此与使用最小化往返时相比，您将在长时间运行的搜索期间获得更准确的进度说明。  3. "_cluster"部分以最终状态开始，根据在每个分片的实际搜索阶段开始之前收集分片信息，显示哪些集群成功或跳过。

使用与上一节相同的设置的示例('ccs_minimize_roundtrips=true')：

    
    
    GET /my-index-000001,cluster_one:my-index-000001,cluster_two:my-index-000001/_async_search?ccs_minimize_roundtrips=false
    {
      "query": {
        "match": {
          "user.id": "kimchy"
        }
      },
      "_source": ["user.id", "message", "http.response.status_code"]
    }

如果查询花费的时间超过"wait_for_completion_timeout"持续时间，API 将返回以下响应(请参阅异步搜索)。

    
    
    {
      "id": "FklQYndoTDJ2VEFlMEVBTzFJMGhJVFEaLVlKYndBWWZSMUdicUc4WVlEaFl4ZzoxNTU=",
      "is_partial": true,
      "is_running": true,
      "start_time_in_millis": 1685563581380,
      "expiration_time_in_millis": 1685995581380,
      "response": {
        "took": 1020,
        "timed_out": false,
        "num_reduce_phases": 0,
        "_shards": {
          "total": 28,     __"successful": 0,
          "failed": 0,
          "skipped": 0
        },
        "_clusters": {
          "total" : 3,
          "successful": 3, __"skipped": 0
        },
        "hits": {
          "total" : {
              "value": 0,
              "relation": "eq"
          },
          "max_score": null,
          "hits": []
        }
      }
    }

__

|

此处列出了搜索范围内所有集群的所有分片。观看此部分以获取用于监视搜索进度的更新。   ---|---    __

|

"_clusters"部分显示已成功从所有 3 个集群中收集分片信息，并且将搜索所有信息(不会跳过任何分片信息)。   ### 可选远程群集编辑

默认情况下，如果请求中的远程集群返回错误或不可用，则跨集群搜索将失败。使用"skip_unavailable"群集设置将特定远程群集标记为跨群集搜索的可选群集。

如果"skip_unavailable"为"true"，则跨集群搜索：

* 如果远程群集的节点在搜索期间不可用，则跳过远程群集。响应的"_cluster.skipped"值包含任何跳过的群集的计数。  * 忽略远程集群返回的错误，例如与不可用分片或索引相关的错误。这可能包括与搜索参数(如"allow_no_indices"和"ignore_unavailable")相关的错误。  * 搜索远程集群时忽略"allow_partial_search_results"参数和相关"search.default_allow_partial_results"集群设置。这意味着远程群集上的搜索可能会返回部分结果。

以下群集更新设置 API 请求将"cluster_two"的"skip_unavailable"设置更改为"true"。

    
    
    PUT _cluster/settings
    {
      "persistent": {
        "cluster.remote.cluster_two.skip_unavailable": true
      }
    }

如果在跨集群搜索期间"cluster_two"断开连接或不可用，Elasticsearch 将不会在最终结果中包含来自该集群的匹配文档。

### 跨集群搜索如何处理网络延迟

由于跨集群搜索涉及向远程集群发送请求，因此任何网络延迟都会影响搜索速度。为了避免搜索速度慢，跨集群搜索提供了两个处理网络延迟的选项：

最大限度地减少网络往返

    

默认情况下，Elasticsearch 会减少远程集群之间的网络往返次数。这减少了网络延迟对搜索速度的影响。但是，Elasticsearch 无法减少大型搜索请求的网络往返，例如包含滚动或 innerhits 的请求。

请参阅最小化网络往返以了解此选项的工作原理。

不要最小化网络往返

    

对于包含滚动或内部命中的搜索请求，Elasticsearch 会向每个远程集群发送多个传出和传入请求。您也可以通过将"ccs_minimize_roundtrips"参数设置为"false"来选择此选项。虽然通常较慢，但此方法可能适用于延迟较低的网络。

请参阅不最小化网络往返以了解此选项的工作原理。

矢量切片搜索 API 始终最小化网络往返，并且不包含"ccs_minimize_roundtrips"参数。

近似 kNN 搜索不支持最小化网络往返，并将参数"ccs_minimize_roundtrips"设置为"false"。

#### 最小化网络往返

下面介绍了在最小化网络往返时跨群集搜索的工作原理。

1. 您向本地集群发送跨集群搜索请求。该群集中的协调节点接收并分析请求。

！CCS 最小往返客户端请求

2. 协调节点向每个集群(包括本地集群)发送单个搜索请求。每个集群独立执行搜索请求，将自己的集群级别设置应用于请求。

！CCS 最小往返集群搜索

3. 每个远程集群将其搜索结果发送回协调节点。

！ccs 最小往返群集结果

4. 从每个集群收集结果后，协调节点在跨集群搜索响应中返回最终结果。

！ccs 最小往返客户端响应

#### 不要最小化网络往返

下面介绍了在不最小化网络往返时跨群集搜索的工作方式。

1. 您向本地集群发送跨集群搜索请求。该群集中的协调节点接收并分析请求。

！CCS 最小往返客户端请求

2. 协调节点向每个远程集群发送"搜索分片"传输层请求，让它们执行"可以匹配"搜索，以确定应搜索每个集群上的哪些分片。

！CCS 最小往返集群搜索

3. 每个远程集群将其响应发送回协调节点。此响应包含有关将对其执行跨集群搜索请求的索引和分片的信息。

！ccs 最小往返群集结果

4. 协调节点向每个分片发送搜索请求，包括其自己集群中的分片。每个分片独立执行搜索请求。

当网络往返未最小化时，将执行搜索，就好像所有数据都在协调节点的群集中一样。我们建议更新限制搜索的群集级别设置，例如"action.search.shard_count.limit"、"pre_filter_shard_size"和"max_concurrent_shard_requests"，以解决此问题。如果这些限制太低，搜索可能会被拒绝。

！CCS 不分钟往返分片搜索

5. 每个分片将其搜索结果发送回协调节点。

！ccs 不分钟往返分片结果

6. 从每个集群收集结果后，协调节点在跨集群搜索响应中返回最终结果。

！ccs 最小往返客户端响应

### 支持的跨集群搜索配置

在 8.0+ 版本中，Elastic 支持从本地集群到远程集群的搜索运行：

* 以前的次要版本。  * 版本相同。  * 同一主要版本中较新的次要版本。

Elastic 还支持从运行主要版本最后一个次要版本的本地集群搜索到运行以下主要版本中任何次要版本的远程集群。例如，本地 7.17 群集可以搜索任何远程 8.x 群集。

|

远程群集版本** ---|--- 本地群集版本**

|

6.8

|

7.1–7.16

|

7.17

|

8.0

|

8.1

|

8.2

|

8.3

|

8.4

|

8.5

|

8.6

|

8.7

|

8.8

|

8.9    6.8

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

!否 7.1–7.16

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

!否 7.17

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!是 8.0

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!是 8.1

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!是 8.2

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!是 8.3

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!是 8.4

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!是 8.5

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!是 8.6

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!是 8.7

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!是 8.8

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!是 8.9

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!是 对于 EQL 搜索 API，如果本地和远程集群的版本低于 7.17.7(包含)或低于 8.5.1(包含)，则必须使用相同的 Elasticsearch 版本。

例如，本地 8.0 群集可以搜索远程 7.17 或任何远程 8.xcluster。但是，不支持从本地 8.0 群集搜索到远程 7.16 或 6.8 群集。

仅支持所有搜索群集中存在的要素。将功能与不支持该功能的远程群集一起使用将导致未定义的行为。

使用不受支持的配置进行跨集群搜索可能仍然有效。但是，此类搜索并未经过 Elastic 的测试，也无法保证其行为。

#### 确保跨集群搜索支持

确保您的集群支持跨集群搜索的最简单方法是将每个集群保留在同一版本的 Elasticsearch 上。如果您需要维护不同版本的集群，您可以：

* 维护一个用于跨集群搜索的专用集群。将此群集保留在搜索其他群集所需的最早版本上。例如，如果您有 7.17 和 8.x 集群，则可以维护一个专用的 7.17 集群，以用作跨集群搜索的本地集群。  * 使每个集群之间的次要版本不超过一个。这允许您在运行跨集群搜索时使用任何集群作为本地集群。

#### 升级期间的跨集群搜索

在本地集群上执行滚动升级时，您仍然可以搜索远程集群。但是，本地协调节点的"从"和"升级到"版本必须与远程集群的网关节点兼容。

不支持在升级持续时间之后在同一集群中运行多个版本的 Elasticsearch。

有关升级的更多信息，请参阅升级弹性搜索。

[« Retrieve selected fields from a search](search-fields.md) [Search
multiple data streams and indices »](search-multiple-indices.md)

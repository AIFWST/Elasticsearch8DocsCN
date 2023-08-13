

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md) ›[Index lifecycle actions](ilm-actions.md)

[« Index lifecycle actions](ilm-actions.md) [Delete »](ilm-delete.md)

##Allocate

允许的阶段：暖，冷。

更新索引设置以更改允许哪些节点托管索引分片并更改副本数。

在热阶段不允许分配操作。索引的初始分配必须手动或通过索引模板完成。

您可以将此操作配置为同时修改分配规则和副本数、仅修改分配规则或仅修改副本数。有关 Elasticsearch 如何使用副本进行扩展的更多信息，请参阅可扩展性和弹性。有关控制 Elasticsearch 分配特定索引的分片位置的更多信息，请参阅索引级分片分配过滤。

###Options

必须指定副本数或至少一个"包含"、"排除"或"要求"选项。空分配操作无效。

有关使用自定义属性进行分片分配的更多信息，请参阅索引级分片分配筛选。

`number_of_replicas`

     (Optional, integer) Number of replicas to assign to the index. 
`total_shards_per_node`

     (Optional, integer) The maximum number of shards for the index on a single Elasticsearch node. A value of `-1` is interpreted as unlimited. See [total shards](allocation-total-shards.html "Total shards per node"). 
`include`

     (Optional, object) Assigns an index to nodes that have at least _one_ of the specified custom attributes. 
`exclude`

     (Optional, object) Assigns an index to nodes that have _none_ of the specified custom attributes. 
`require`

     (Optional, object) Assigns an index to nodes that have _all_ of the specified custom attributes. 

###Example

以下策略中的分配操作将索引的副本数更改为"2"。索引的分片不会超过200个放置在任何单个节点上。否则，不会更改索引分配规则。

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          phases: {
            warm: {
              actions: {
                allocate: {
                  number_of_replicas: 2,
                  total_shards_per_node: 200
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT _ilm/policy/my_policy
    {
      "policy": {
        "phases": {
          "warm": {
            "actions": {
              "allocate" : {
                "number_of_replicas" : 2,
                "total_shards_per_node" : 200
              }
            }
          }
        }
      }
    }

#### 使用自定义属性将索引分配给节点

以下策略中的分配操作将索引分配给"box_type"为 _hot_ 或 _warm_ 的节点。

要指定节点的"box_type"，请在节点配置中设置自定义属性。例如，在"elasticsearch.yml"中设置"node.attr.box_type：hot"。有关更多信息，请参阅 启用索引级分片分配筛选。

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          phases: {
            warm: {
              actions: {
                allocate: {
                  include: {
                    box_type: 'hot,warm'
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT _ilm/policy/my_policy
    {
      "policy": {
        "phases": {
          "warm": {
            "actions": {
              "allocate" : {
                "include" : {
                  "box_type": "hot,warm"
                }
              }
            }
          }
        }
      }
    }

#### 根据多个属性为节点分配索引

分配操作还可以根据多个节点属性将索引分配给节点。以下操作根据"box_type"和"存储"节点属性分配索引。

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          phases: {
            cold: {
              actions: {
                allocate: {
                  require: {
                    box_type: 'cold',
                    storage: 'high'
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT _ilm/policy/my_policy
    {
      "policy": {
        "phases": {
          "cold": {
            "actions": {
              "allocate" : {
                "require" : {
                  "box_type": "cold",
                  "storage": "high"
                }
              }
            }
          }
        }
      }
    }

#### 将索引分配给特定节点并更新副本设置

以下策略中的分配操作会将索引更新为每个分片一个副本，并分配给"box_type"为 _cold_ 的节点。

要指定节点的"box_type"，请在节点配置中设置自定义属性。例如，在"elasticsearch.yml"中设置"node.attr.box_type：cold"。有关更多信息，请参阅 启用索引级分片分配筛选。

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          phases: {
            warm: {
              actions: {
                allocate: {
                  number_of_replicas: 1,
                  require: {
                    box_type: 'cold'
                  }
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT _ilm/policy/my_policy
    {
      "policy": {
        "phases": {
          "warm": {
            "actions": {
              "allocate" : {
                "number_of_replicas": 1,
                "require" : {
                  "box_type": "cold"
                }
            }
            }
          }
        }
      }
    }

[« Index lifecycle actions](ilm-actions.md) [Delete »](ilm-delete.md)



[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md) ›[Index lifecycle actions](ilm-actions.md)

[« Read only](ilm-readonly.md) [Downsample »](ilm-downsample.md)

##Rollover

允许的阶段：热。

当现有索引满足指定的滚动更新条件时，将目标滚动更新到新索引。

如果对追随者索引使用翻转操作，则策略执行将等待，直到领导者索引滚动更新(或以其他方式标记为完成)，然后使用取消关注操作将追随者索引转换为常规索引。

滚动更新目标可以是数据流或索引别名。以数据流为目标时，新索引将成为数据流的写入索引，并且其生成递增。

要滚动更新索引别名，别名及其写入索引必须满足以下条件：

* 索引名称必须与模式 _^.*-\d+$_ 匹配，例如 ('my-index-000001')。  * 必须将"index.lifecycle.rollover_alias"配置为要滚动更新的别名。  * 索引必须是别名的写入索引。

例如，如果"my-index-000001"具有别名"my_data"，则必须配置以下设置。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          "index.lifecycle.name": 'my_policy',
          "index.lifecycle.rollover_alias": 'my_data'
        },
        aliases: {
          my_data: {
            is_write_index: true
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "settings": {
        "index.lifecycle.name": "my_policy",
        "index.lifecycle.rollover_alias": "my_data"
      },
      "aliases": {
        "my_data": {
          "is_write_index": true
        }
      }
    }

###Options

翻转操作必须指定至少一个 max_* 条件，它可以包括零个或多个min_* 条件。空翻转操作无效。

一旦满足任何max_*条件并且满足所有min_*条件，指数将展期。但请注意，默认情况下不会滚动更新空索引。

`max_age`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Triggers rollover after the maximum elapsed time from index creation is reached. The elapsed time is always calculated since the index creation time, even if the index origination date is configured to a custom date, such as when using the [index.lifecycle.parse_origination_date](ilm-settings.html#index-lifecycle-parse-origination-date) or [index.lifecycle.origination_date](ilm-settings.html#index-lifecycle-origination-date) settings. 
`max_docs`

     (Optional, integer) Triggers rollover after the specified maximum number of documents is reached. Documents added since the last refresh are not included in the document count. The document count does **not** include documents in replica shards. 
`max_size`

    

(可选，字节单位)当索引达到特定大小时触发滚动更新。这是索引中所有主分片的总大小。副本不计入最大索引大小。

若要查看当前索引大小，请使用_cat索引 API。"pri.store.size"值显示所有主分片的组合大小。

`max_primary_shard_size`

    

(可选，字节单位)当索引中最大的主分片达到特定大小时触发滚动更新。这是索引中主分片的最大大小。与"max_size"一样，副本将被忽略。

要查看当前分片大小，请使用_cat分片 API。"store"值显示每个分片的大小，"prirep"表示分片是主分片("p")还是副本("r")。

`max_primary_shard_docs`

    

(可选，整数)当索引中最大的主分片达到一定数量的文档时触发滚动更新。这是索引中主分片的最大文档数。与"max_docs"一样，副本将被忽略。

要查看当前的分片文档，请使用_cat分片 API。"docs"值显示每个分片的文档数量。

`min_age`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Prevents rollover until after the minimum elapsed time from index creation is reached. See notes on `max_age`. 
`min_docs`

     (Optional, integer) Prevents rollover until after the specified minimum number of documents is reached. See notes on `max_docs`. 
`min_size`

     (Optional, [byte units](api-conventions.html#byte-units "Byte size units")) Prevents rollover until the index reaches a certain size. See notes on `max_size`. 
`min_primary_shard_size`

     (Optional, [byte units](api-conventions.html#byte-units "Byte size units")) Prevents rollover until the largest primary shard in the index reaches a certain size. See notes on `max_primary_shard_size`. 
`min_primary_shard_docs`

     (Optional, integer) Prevents rollover until the largest primary shard in the index reaches a certain number of documents. See notes on `max_primary_shard_docs`. 

空索引不会被滚动更新，即使它们具有关联的"max_age"，否则会导致发生滚动更新。策略可以覆盖此行为，并通过添加"min_docs"：0"条件显式选择滚动空索引。也可以通过将"indices.lifecycle.rollover.only_if_has_documents"设置为"false"在群集范围内禁用此功能。

如果一个或多个分片包含 200000000 个或更多文档，则滚动更新操作始终隐式滚动更新数据流或别名。通常，一个分片在达到 2 亿个文档之前会达到 50GB，但对于空间高效的数据集来说，情况并非如此。如果 ashard 包含超过 2 亿个文档，则搜索性能很可能会受到影响。这就是内置限制的原因。

###Example

#### 基于最大主分片大小进行滚动更新

此示例在其最大主分片至少为 50 GB 时滚动更新索引。

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          phases: {
            hot: {
              actions: {
                rollover: {
                  max_primary_shard_size: '50gb'
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
          "hot": {
            "actions": {
              "rollover" : {
                "max_primary_shard_size": "50gb"
              }
            }
          }
        }
      }
    }

#### 基于索引大小进行翻转

本示例在索引至少为 100 GB 时滚动更新索引。

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          phases: {
            hot: {
              actions: {
                rollover: {
                  max_size: '100gb'
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
          "hot": {
            "actions": {
              "rollover" : {
                "max_size": "100gb"
              }
            }
          }
        }
      }
    }

#### 基于文档计数进行滚动更新

本示例在索引至少包含一亿个文档时滚动更新索引。

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          phases: {
            hot: {
              actions: {
                rollover: {
                  max_docs: 100_000_000
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
          "hot": {
            "actions": {
              "rollover" : {
                "max_docs": 100000000
              }
            }
          }
        }
      }
    }

#### 根据最大主分片的文档计数进行滚动更新

此示例在索引包含最大主分片的至少 1000 万个文档时滚动更新索引。

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          phases: {
            hot: {
              actions: {
                rollover: {
                  max_primary_shard_docs: 10_000_000
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
          "hot": {
            "actions": {
              "rollover" : {
                "max_primary_shard_docs": 10000000
              }
            }
          }
        }
      }
    }

#### 基于索引的滚动更新

如果索引是在至少 7 天前创建的，则此示例将滚动更新索引。

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          phases: {
            hot: {
              actions: {
                rollover: {
                  max_age: '7d'
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
          "hot": {
            "actions": {
              "rollover" : {
                "max_age": "7d"
              }
            }
          }
        }
      }
    }

#### 使用多个条件进行翻转

指定多个翻转条件时，索引将滚动更新when_any_max_* 和 _all_ 的 min_* 条件。如果索引至少存在 7 天或至少为 100 GB，则此示例将索引滚动，但前提是索引至少包含 1000 个文档。

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          phases: {
            hot: {
              actions: {
                rollover: {
                  max_age: '7d',
                  max_size: '100gb',
                  min_docs: 1000
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
          "hot": {
            "actions": {
              "rollover" : {
                "max_age": "7d",
                "max_size": "100gb",
                "min_docs": 1000
              }
            }
          }
        }
      }
    }

#### 在保持分片大小的同时滚动更新

此示例在主分片大小至少为 50gb 或索引至少存在 30 天(但只要主分片至少为 1gb)时滚动更新索引。对于低容量索引，这可以防止创建许多小分片。

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          phases: {
            hot: {
              actions: {
                rollover: {
                  max_primary_shard_size: '50gb',
                  max_age: '30d',
                  min_primary_shard_size: '1gb'
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
          "hot": {
            "actions": {
              "rollover" : {
                "max_primary_shard_size": "50gb",
                "max_age": "30d",
                "min_primary_shard_size": "1gb"
              }
            }
          }
        }
      }
    }

#### 翻转条件阻止相变

仅当满足其中一个条件时，翻转操作才会完成。这意味着任何后续阶段都将被阻止，直到翻转成功。

例如，以下策略在索引滚动更新一天后将其删除。它不会在创建索引一天后删除索引。

    
    
    response = client.ilm.put_lifecycle(
      policy: 'rollover_policy',
      body: {
        policy: {
          phases: {
            hot: {
              actions: {
                rollover: {
                  max_size: '50gb'
                }
              }
            },
            delete: {
              min_age: '1d',
              actions: {
                delete: {}
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /_ilm/policy/rollover_policy
    {
      "policy": {
        "phases": {
          "hot": {
            "actions": {
              "rollover": {
                "max_size": "50gb"
              }
            }
          },
          "delete": {
            "min_age": "1d",
            "actions": {
              "delete": {}
            }
          }
        }
      }
    }

[« Read only](ilm-readonly.md) [Downsample »](ilm-downsample.md)

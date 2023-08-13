

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[How
to](how-to.md)

[« Tune for indexing speed](tune-for-indexing-speed.md) [Tune approximate
kNN search »](tune-knn-search.md)

## 调整搜索速度

### 为文件系统缓存提供内存

Elasticsearch严重依赖文件系统缓存来实现搜索速度。一般来说，你应该确保至少有一半的可用内存进入文件系统缓存，以便 Elasticsearch 可以将索引的热区域保留在物理内存中。

### 通过在 Linux 上使用适度的预读值来避免页面缓存抖动

搜索可能会导致大量随机读取 I/O。当底层块设备具有较高的预读值时，可能会有很多不必要的读取 I/Odone，尤其是在使用内存映射访问文件时(请参阅存储类型)。

大多数Linux发行版对单个普通设备使用合理的预读值"128KiB"，但是，当使用软件raid，LVM或dm-crypt时，生成的块设备(支持Elasticsearch path.data)最终可能会具有非常大的预读值(在几个MiB的范围内)。这通常会导致严重的页面(文件系统)缓存抖动，从而对搜索(或更新)性能产生负面影响。

您可以使用"lsblk -oNAME，RA，MOUNTPOINT，TYPE，SIZE"检查"KiB"中的当前值。请参阅发行版的文档，了解如何更改此值(例如，使用"udev"规则来持久化交叉重启，或通过 blockdev --setra 作为瞬态设置)。我们建议预读的值为"128KiB"。

"blockdev"期望值在512字节扇区中，而"lsblk"报告"KiB"中的值。例如，要暂时将预读设置为"128KiB"，for'/dev/nvme0n1'，请指定"blockdev --setra 256 /dev/nvme0n1"。

### 使用更快的硬件

如果您的搜索是 I/O 密集型的，请考虑增加文件系统缓存的大小(见上文)或使用更快的存储。每次搜索都涉及跨多个文件的顺序和随机读取的混合，并且每个分片上可能同时运行许多搜索，因此 SSD 驱动器的性能往往优于旋转磁盘。

直连(本地)存储通常比远程存储性能更好，因为它更易于配置，并且避免了通信开销。通过仔细调整，有时也可以使用远程存储实现可接受的性能。使用实际工作负载对系统进行基准测试，以确定任何调优参数的影响。如果无法达到预期的性能，请与存储系统的供应商联系以确定问题所在。

如果搜索受 CPU 限制，请考虑使用更多速度更快的 CPU。

### 文档建模

应对文档进行建模，以便搜索时操作尽可能便宜。

特别是，应避免联接。"嵌套"可以使查询慢几倍，父子关系可以使查询慢数百倍。因此，如果可以通过非规范化文档来回答相同的问题，则可以预期显著的加速。

### 搜索尽可能少的字段

"query_string"或"multi_match"查询定位的字段越多，速度就越慢。提高多个字段的搜索速度的常用方法是在索引时将其值复制到单个字段中，然后在搜索时使用此字段。这可以通过映射的"复制到"指令自动完成，而无需更改文档的来源。下面是一个包含索引的电影示例，该示例通过将两个值索引到"name_and_plot"字段中来优化搜索电影名称和情节的查询。

    
    
    response = client.indices.create(
      index: 'movies',
      body: {
        mappings: {
          properties: {
            name_and_plot: {
              type: 'text'
            },
            name: {
              type: 'text',
              copy_to: 'name_and_plot'
            },
            plot: {
              type: 'text',
              copy_to: 'name_and_plot'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT movies
    {
      "mappings": {
        "properties": {
          "name_and_plot": {
            "type": "text"
          },
          "name": {
            "type": "text",
            "copy_to": "name_and_plot"
          },
          "plot": {
            "type": "text",
            "copy_to": "name_and_plot"
          }
        }
      }
    }

### 预索引数据

应在查询中利用模式来优化数据编制索引的方式。例如，如果您的所有文档都有一个"价格"字段，并且大多数查询在固定的范围列表上运行"范围"聚合，则可以通过将范围预先索引到索引中并使用"terms"聚合来加快此聚合。

例如，如果文档如下所示：

    
    
    response = client.index(
      index: 'index',
      id: 1,
      body: {
        designation: 'spoon',
        price: 13
      }
    )
    puts response
    
    
    PUT index/_doc/1
    {
      "designation": "spoon",
      "price": 13
    }

搜索请求如下所示：

    
    
    response = client.search(
      index: 'index',
      body: {
        aggregations: {
          price_ranges: {
            range: {
              field: 'price',
              ranges: [
                {
                  to: 10
                },
                {
                  from: 10,
                  to: 100
                },
                {
                  from: 100
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    GET index/_search
    {
      "aggs": {
        "price_ranges": {
          "range": {
            "field": "price",
            "ranges": [
              { "to": 10 },
              { "from": 10, "to": 100 },
              { "from": 100 }
            ]
          }
        }
      }
    }

然后，可以在索引时通过"price_range"字段来丰富文档，该字段应映射为"关键字"：

    
    
    response = client.indices.create(
      index: 'index',
      body: {
        mappings: {
          properties: {
            price_range: {
              type: 'keyword'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'index',
      id: 1,
      body: {
        designation: 'spoon',
        price: 13,
        price_range: '10-100'
      }
    )
    puts response
    
    
    PUT index
    {
      "mappings": {
        "properties": {
          "price_range": {
            "type": "keyword"
          }
        }
      }
    }
    
    PUT index/_doc/1
    {
      "designation": "spoon",
      "price": 13,
      "price_range": "10-100"
    }

然后，搜索请求可以聚合此新字段，而不是在"价格"字段上运行"范围"聚合。

    
    
    response = client.search(
      index: 'index',
      body: {
        aggregations: {
          price_ranges: {
            terms: {
              field: 'price_range'
            }
          }
        }
      }
    )
    puts response
    
    
    GET index/_search
    {
      "aggs": {
        "price_ranges": {
          "terms": {
            "field": "price_range"
          }
        }
      }
    }

### 考虑将标识符映射为"关键字"

并非所有数值数据都应映射为数值字段数据类型。Elasticsearch 为"range"查询优化数值字段，例如"整数"或"long"。但是，"关键字"字段更适合"术语"和其他术语级查询。

标识符(如 ISBN 或产品 ID)很少在"范围"查询中使用。但是，它们通常使用术语级查询进行检索。

在以下情况下，请考虑将数字标识符映射为"关键字"：

* 您不打算使用"范围"查询搜索标识符数据。  * 快速检索很重要。对"关键字"字段的"术语"查询搜索通常比对数值字段的"术语"搜索更快。

如果不确定要使用哪个，可以使用多字段将数据映射为"关键字"_和_数字数据类型。

### 避免脚本

如果可能，请避免使用基于脚本的排序、聚合中的脚本和"script_score"查询。请参阅脚本、缓存和搜索速度。

### 搜索舍入日期

对使用"now"的日期字段的查询通常不可缓存，因为匹配的范围一直在变化。但是，就用户体验而言，切换到环绕日期通常是可以接受的，并且具有更好地利用查询缓存的好处。

例如，以下查询：

    
    
    response = client.index(
      index: 'index',
      id: 1,
      body: {
        my_date: '2016-05-11T16:30:55.328Z'
      }
    )
    puts response
    
    response = client.search(
      index: 'index',
      body: {
        query: {
          constant_score: {
            filter: {
              range: {
                my_date: {
                  gte: 'now-1h',
                  lte: 'now'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT index/_doc/1
    {
      "my_date": "2016-05-11T16:30:55.328Z"
    }
    
    GET index/_search
    {
      "query": {
        "constant_score": {
          "filter": {
            "range": {
              "my_date": {
                "gte": "now-1h",
                "lte": "now"
              }
            }
          }
        }
      }
    }

可以替换为以下查询：

    
    
    response = client.search(
      index: 'index',
      body: {
        query: {
          constant_score: {
            filter: {
              range: {
                my_date: {
                  gte: 'now-1h/m',
                  lte: 'now/m'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET index/_search
    {
      "query": {
        "constant_score": {
          "filter": {
            "range": {
              "my_date": {
                "gte": "now-1h/m",
                "lte": "now/m"
              }
            }
          }
        }
      }
    }

在这种情况下，我们四舍五入到分钟，因此如果当前时间为"16：31：29"，则范围查询将匹配"my_date"字段值介于"15：31：00"和"16：31：59"之间的所有内容。如果多个用户在同一分钟内运行包含此范围的查询，则查询缓存可以帮助加快速度。用于舍入的间隔越长，查询缓存的帮助就越大，但请注意，过于激进的舍入也可能损害用户体验。

为了能够利用查询缓存，将范围拆分为较大的可缓存部分和较小的不可缓存部分可能很诱人，如下所示：

    
    
    response = client.search(
      index: 'index',
      body: {
        query: {
          constant_score: {
            filter: {
              bool: {
                should: [
                  {
                    range: {
                      my_date: {
                        gte: 'now-1h',
                        lte: 'now-1h/m'
                      }
                    }
                  },
                  {
                    range: {
                      my_date: {
                        gt: 'now-1h/m',
                        lt: 'now/m'
                      }
                    }
                  },
                  {
                    range: {
                      my_date: {
                        gte: 'now/m',
                        lte: 'now'
                      }
                    }
                  }
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET index/_search
    {
      "query": {
        "constant_score": {
          "filter": {
            "bool": {
              "should": [
                {
                  "range": {
                    "my_date": {
                      "gte": "now-1h",
                      "lte": "now-1h/m"
                    }
                  }
                },
                {
                  "range": {
                    "my_date": {
                      "gt": "now-1h/m",
                      "lt": "now/m"
                    }
                  }
                },
                {
                  "range": {
                    "my_date": {
                      "gte": "now/m",
                      "lte": "now"
                    }
                  }
                }
              ]
            }
          }
        }
      }
    }

但是，在某些情况下，这种做法可能会使查询运行速度变慢，因为"bool"查询引入的开销可能会破坏更好地利用查询缓存所节省的成本。

### 强制合并只读索引

只读索引可能会受益于合并到单个段。基于时间的索引通常就是这种情况：只有当前时间范围的索引获取新文档，而旧索引是只读的。已强制合并到单个段中的分片可以使用更简单、更高效的数据结构来执行搜索。

不要强制合并仍在写入的索引，或者将来将再次写入的索引。相反，请依靠自动后台合并过程根据需要执行合并，以保持索引平稳运行。如果您继续写入强制合并的索引，那么它的性能可能会变得更糟。

### 预热全局序数

全局序数是用于优化聚合性能的数据结构。它们是延迟计算的，并作为字段数据缓存的一部分存储在 JVM 堆中。对于大量用于分桶聚合的字段，您可以告诉 Elasticsearch 在收到请求之前构造和缓存全局序数。应谨慎执行此操作，因为它会增加堆使用率，并且刷新时间更长。通过设置预先全局序数映射参数，可以在现有映射上动态更新该选项：

    
    
    response = client.indices.create(
      index: 'index',
      body: {
        mappings: {
          properties: {
            foo: {
              type: 'keyword',
              eager_global_ordinals: true
            }
          }
        }
      }
    )
    puts response
    
    
    PUT index
    {
      "mappings": {
        "properties": {
          "foo": {
            "type": "keyword",
            "eager_global_ordinals": true
          }
        }
      }
    }

### 预热文件系统缓存

如果运行 Elasticsearch 的计算机重新启动，文件系统缓存将为空，因此操作系统需要一些时间才能将索引的热区域加载到内存中，以便快速执行搜索操作。您可以使用"index.store.preload"设置根据文件扩展名显式告诉操作系统哪些文件应该加载到内存中。

如果文件系统缓存不够大，无法容纳所有数据，则在太多索引或太多文件上急切地将数据加载到文件系统缓存中将使搜索_变慢_。请谨慎使用。

### 使用索引排序来加速上合

索引排序可能很有用，以便以稍微慢索引的速度进行连词。在索引排序文档中阅读有关它的更多信息。

### 使用"首选项"优化缓存利用率

有多个缓存可以帮助提高搜索性能，例如文件系统缓存、请求缓存或查询缓存。然而，所有这些缓存都是在节点级别维护的，这意味着如果您连续两次运行相同的请求，拥有 1 个副本或更多副本并使用默认路由算法轮询，那么这两个请求将转到不同的分片副本，从而防止节点级缓存提供帮助。

由于搜索应用程序的用户通常会一个接一个地运行类似的请求，例如为了分析索引的较窄子集，因此使用标识当前用户或会话的首选项值可以帮助优化缓存的使用。

### 副本可能有助于提高吞吐量，但并非总是如此

除了提高复原能力外，副本还有助于提高吞吐量。例如，如果您有一个单分片索引和三个节点，则需要将副本数设置为 2，以便拥有 3 个分片总计副本，以便利用所有节点。

现在假设您有一个 2 分片索引和两个节点。在一种情况下，副本数为 0，这意味着每个节点持有一个分片。在第二种情况下，副本数为 1，这意味着每个节点有两个分片。哪种设置在搜索性能方面表现最佳？通常，每个节点总共具有较少分片的设置将执行得更好。原因是它为每个分片提供了更大的可用文件系统缓存份额，并且文件系统缓存可能是Elasticsearch的第一大性能因素。同时，请注意，没有副本的安装程序在单节点发生故障时会失败，因此需要在吞吐量和可用性之间进行权衡。

那么正确的副本数量是多少？如果您的集群具有"num_nodes"节点，_in total_"num_primaries"主分片，并且如果您希望能够最多一次处理"max_failures"节点故障，那么适合您的副本数是"max(max_failures，ceil(num_nodes /num_primaries) - 1)"。

### 使用搜索探查器调整查询

配置文件 API 提供有关查询和聚合的每个组件如何影响处理请求所需的时间的详细信息。

Kibana 中的搜索探查器使您可以轻松导航和分析配置文件结果，并让您深入了解如何调整查询以提高性能和减少负载。

由于配置文件 API 本身会给查询增加大量开销，因此此信息最适合用于了解各种查询组件的相对成本。它不能提供实际处理时间的可靠度量。

### 使用"index_phrases"进行更快的短语查询

"text"字段有一个"index_phrases"选项，该选项索引 2 带状疱疹，并由查询解析器自动利用来运行没有 slop 的短语查询。如果您的用例涉及运行大量短语查询，这可以显着加快查询速度。

### 使用"index_prefixes"进行更快的前缀查询

"text"字段有一个"index_prefixes"选项，该选项为所有术语的前缀编制索引，并由查询解析器自动用于运行前缀查询。如果您的用例涉及运行大量前缀查询，这可以显着加快查询速度。

### 使用"constant_keyword"加快上过滤速度

有一个一般规则，即筛选器的成本主要是匹配文档数量的函数。假设您有一个包含周期的索引。有大量的自行车，许多搜索对"cycle_type：自行车"执行过滤器。不幸的是，这种非常常见的过滤器也非常昂贵，因为它与大多数文档匹配。有一种简单的方法可以避免运行此筛选器：将自行车移动到其自己的索引，并通过搜索此索引而不是向查询添加筛选器来筛选自行车。

不幸的是，这可能会使客户端逻辑变得棘手，这就是"constant_keyword"的帮助所在。通过在包含自行车的索引上将"cycle_type"映射为值为"bike"的"constant_keyword"，客户端可以继续运行与在整体索引上运行完全相同的查询，并且Elasticsearch将通过忽略"cycle_type"上的过滤器(如果值为"bike")并且不返回任何命中来对自行车索引执行正确的操作。

映射可能如下所示：

    
    
    response = client.indices.create(
      index: 'bicycles',
      body: {
        mappings: {
          properties: {
            cycle_type: {
              type: 'constant_keyword',
              value: 'bicycle'
            },
            name: {
              type: 'text'
            }
          }
        }
      }
    )
    puts response
    
    response = client.indices.create(
      index: 'other_cycles',
      body: {
        mappings: {
          properties: {
            cycle_type: {
              type: 'keyword'
            },
            name: {
              type: 'text'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT bicycles
    {
      "mappings": {
        "properties": {
          "cycle_type": {
            "type": "constant_keyword",
            "value": "bicycle"
          },
          "name": {
            "type": "text"
          }
        }
      }
    }
    
    PUT other_cycles
    {
      "mappings": {
        "properties": {
          "cycle_type": {
            "type": "keyword"
          },
          "name": {
            "type": "text"
          }
        }
      }
    }

我们将索引一分为二：一个仅包含自行车，另一个包含其他周期：独轮车、三轮车等。然后在搜索时，我们需要搜索两个索引，但我们不需要修改查询。

    
    
    response = client.search(
      index: 'bicycles,other_cycles',
      body: {
        query: {
          bool: {
            must: {
              match: {
                description: 'dutch'
              }
            },
            filter: {
              term: {
                cycle_type: 'bicycle'
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET bicycles,other_cycles/_search
    {
      "query": {
        "bool": {
          "must": {
            "match": {
              "description": "dutch"
            }
          },
          "filter": {
            "term": {
              "cycle_type": "bicycle"
            }
          }
        }
      }
    }

在"自行车"索引上，Elasticsearch 将简单地忽略"cycle_type"过滤器，并将搜索请求重写为下面的一个：

    
    
    response = client.search(
      index: 'bicycles,other_cycles',
      body: {
        query: {
          match: {
            description: 'dutch'
          }
        }
      }
    )
    puts response
    
    
    GET bicycles,other_cycles/_search
    {
      "query": {
        "match": {
          "description": "dutch"
        }
      }
    }

在"other_cycles"索引上，Elasticsearch 将很快发现"自行车"在"cycle_type"字段的术语字典中不存在，并返回没有命中的搜索响应。

这是一种通过将通用值放在专用索引中来降低查询成本的有效方法。这个想法也可以跨多个领域组合：例如，如果你跟踪每个周期的颜色，并且你的"自行车"指数最终拥有大多数黑色自行车，你可以将其拆分为"自行车黑色"和"自行车其他颜色"指数。

此优化并不严格要求"constant_keyword"：还可以更新客户端逻辑，以便根据过滤器将查询路由到相关索引。但是，"constant_keyword"使其透明化，并允许将搜索请求与索引拓扑分离，以换取很少的开销。

[« Tune for indexing speed](tune-for-indexing-speed.md) [Tune approximate
kNN search »](tune-knn-search.md)

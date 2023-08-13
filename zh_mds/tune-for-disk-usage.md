

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[How
to](how-to.md)

[« Tune approximate kNN search](tune-knn-search.md) [Size your shards
»](size-your-shards.md)

## 调整磁盘使用情况

### 禁用您不需要的功能

默认情况下，Elasticsearch 会索引文档值并将其添加到大多数字段中，以便可以开箱即用地搜索和聚合它们。例如，如果您有一个名为"foo"的数值字段，您需要在其上运行直方图，但您永远不需要对其进行过滤，则可以安全地禁用此字段的索引：

    
    
    response = client.indices.create(
      index: 'index',
      body: {
        mappings: {
          properties: {
            foo: {
              type: 'integer',
              index: false
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
            "type": "integer",
            "index": false
          }
        }
      }
    }

"文本"字段在索引中存储规范化因子，以便于文档评分。如果您只需要"文本"字段上的匹配功能，但不关心生成的分数，则可以改用"match_only_text"类型。此字段类型通过删除评分和位置信息来节省大量空间。

### 不要使用默认的动态字符串映射

默认动态字符串映射将索引字符串字段作为"文本"和"关键字"。如果您只需要其中之一，这是浪费。通常，"id"字段只需要作为"关键字"编制索引，而"body"字段只需要作为"文本"字段编制索引。

可以通过在字符串字段上配置显式映射或设置将字符串字段映射为"文本"或"关键字"的动态模板来禁用此功能。

例如，这里有一个模板，可用于仅将字符串字段映射为"关键字"：

    
    
    response = client.indices.create(
      index: 'index',
      body: {
        mappings: {
          dynamic_templates: [
            {
              strings: {
                match_mapping_type: 'string',
                mapping: {
                  type: 'keyword'
                }
              }
            }
          ]
        }
      }
    )
    puts response
    
    
    PUT index
    {
      "mappings": {
        "dynamic_templates": [
          {
            "strings": {
              "match_mapping_type": "string",
              "mapping": {
                "type": "keyword"
              }
            }
          }
        ]
      }
    }

### 注意分片大小

更大的分片在存储数据方面将更有效率。要增加分片的大小，您可以通过创建主分片较少的索引、创建较少的索引(例如，利用 RolloverAPI)或使用收缩 API 修改现有索引来减少索引中的主分片数量。

请记住，较大的分片大小也有缺点，例如完整恢复时间长。

### 禁用"_source"

"_source"字段存储文档的原始 JSON 正文。如果您不需要访问它，则可以禁用它。但是，需要访问"_source"(如更新、突出显示和重新索引)的 API 将不起作用。

### 使用"best_compression"

"_source"和存储字段很容易占用不可忽略的磁盘空间量。可以使用"best_compression"编解码器更积极地压缩它们。

### 强制合并

Elasticsearch 中的索引存储在一个或多个分片中。每个分片都是Lucene索引，由一个或多个段组成 - 磁盘上的实际文件。较大的段存储数据的效率更高。

强制合并 API 可用于减少每个分片的段数。在许多情况下，可以通过设置"max_num_segments=1"将段数减少到每个分片一个。

**我们建议仅强制合并只读索引(意味着索引不再接收写入)。** 更新或删除文档时，旧版本不会立即删除，而是软删除并标有"逻辑删除"。这些软删除的文档会在常规段合并期间自动清理。但是强制合并可能会导致产生非常大(> 5GB)的段，这些段不符合常规合并的条件。因此，软删除文档的数量可能会快速增长，从而导致磁盘使用率更高，搜索性能更差。如果定期强制合并索引接收写入，这也会使快照更加昂贵，因为新文档无法增量备份。

### 收缩指数

收缩 API 允许您减少索引中的分片数量。与上面的强制合并 API 一起，这可以显着减少 anindex 的分片和段数。

### 使用足够的最小数值类型

为数值数据选择的类型可能会对磁盘使用情况产生重大影响。特别是，整数应使用整数类型("字节"、"短"、"整数"或"长")进行存储，并且浮点应存储在"scaled_float"中(如果适用)，或者存储在适合用例的最小类型中：在"双精度"上使用"float"，或在"float"上使用"half_float"将有助于节省存储空间。

### 使用索引排序共置相似文档

当 Elasticsearch 存储"_source"时，它会一次压缩多个文档以提高整体压缩率。例如，文档共享相同的字段名称是非常常见的，并且它们共享一些字段值也很常见，尤其是在基数或 azipfian 分布较低的字段上。

默认情况下，文档按照添加到索引中的顺序压缩在一起。如果启用了索引排序，则按排序顺序压缩它们。将具有相似结构、字段和值的文档排序在一起应该可以提高压缩率。

### 将字段按相同的顺序放入文档中

由于多个文档被压缩成块，如果字段始终以相同的顺序出现，则更有可能在这些"_source"文档中找到更长的重复字符串。

### 汇总历史数据

保留较旧的数据对于以后的分析很有用，但由于存储成本，通常会避免使用。您可以使用数据汇总来汇总和存储历史数据，而成本仅为原始数据的一小部分。请参阅_Rolling historicaldata_。

[« Tune approximate kNN search](tune-knn-search.md) [Size your shards
»](size-your-shards.md)



[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Field data types](mapping-types.md)

[« Unsigned long field type](unsigned-long.md) [Metadata fields »](mapping-
fields.md)

## 版本字段类型

"版本"字段类型是"关键字"字段的专用化，用于处理软件版本值并支持它们的专用优先级规则。优先级是根据 SemanticVersion 概述的规则定义的，例如，这意味着主要、次要补丁版本部分按数字排序(即"2.1.0"<"2.4.1"<"2.11.2")，预发布版本在发布版本之前排序(即"1.0.0-alpha"<"1.0.0")。

按如下方式为"版本"字段编制索引

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            my_version: {
              type: 'version'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001
    {
      "mappings": {
        "properties": {
          "my_version": {
            "type": "version"
          }
        }
      }
    }

该字段提供与常规关键字字段相同的搜索功能。例如，可以使用"匹配"或"术语"查询搜索完全匹配，并支持前缀和通配符搜索。主要好处是"范围"查询将遵循 Semver 排序，因此"1.0.0"和"1.5.0"之间的"范围"查询将包括"1.2.3"的版本，但不包括"1.11.2"的版本。请注意，当使用常规的"关键字"字段进行索引时，这将有所不同，其中排序是按字母顺序排列的。

软件版本应遵循语义版本控制规则架构和优先规则，但值得注意的是，允许或少于三个主要版本标识符(即"1.2"或"1.2.3.4"符合有效版本，而它们不会低于严格的 Semver 规则)。在 Semverdefinition 下无效的版本字符串(例如"1.2.alpha.4")仍然可以作为精确匹配进行索引和检索，但是它们都将出现在任何具有常规字母顺序的有效版本中。空字符串 "" 被视为无效，并在所有有效版本之后排序，但在其他无效版本之前排序。

#### 版本字段的参数

"版本"字段接受以下参数：

"元"

|

有关字段的元数据。   ---|--- ####Limitationsedit

此字段类型未针对繁重的通配符、正则表达式或模糊搜索进行优化。虽然这些类型的查询在此字段中有效，但如果您强烈依赖这些类型的查询，则应考虑使用常规的"关键字"字段。

### 合成的"_source"

合成"_source"仅对 TSDB 索引(将"index.mode"设置为"time_series"的索引)正式发布。对于其他指数，合成"_source"处于技术预览状态。技术预览版中的功能可能会在将来的版本中更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

"版本"字段支持合成的"_source"，只要它们不声明"copy_to"。

合成源始终对"版本"字段进行排序并删除重复项。例如：

    
    
    response = client.indices.create(
      index: 'idx',
      body: {
        mappings: {
          _source: {
            mode: 'synthetic'
          },
          properties: {
            versions: {
              type: 'version'
            }
          }
        }
      }
    )
    puts response
    
    response = client.index(
      index: 'idx',
      id: 1,
      body: {
        versions: [
          '8.0.0-beta1',
          '8.5.0',
          '0.90.12',
          '2.6.1',
          '1.3.4',
          '1.3.4'
        ]
      }
    )
    puts response
    
    
    PUT idx
    {
      "mappings": {
        "_source": { "mode": "synthetic" },
        "properties": {
          "versions": { "type": "version" }
        }
      }
    }
    PUT idx/_doc/1
    {
      "versions": ["8.0.0-beta1", "8.5.0", "0.90.12", "2.6.1", "1.3.4", "1.3.4"]
    }

将成为：

    
    
    {
      "versions": ["0.90.12", "1.3.4", "2.6.1", "8.0.0-beta1", "8.5.0"]
    }

[« Unsigned long field type](unsigned-long.md) [Metadata fields »](mapping-
fields.md)

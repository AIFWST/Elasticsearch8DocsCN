

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `normalizer`](normalizer.md) [`null_value` »](null-value.md)

##'规范'

规范存储各种规范化因子，稍后在查询时使用，以便计算文档相对于查询的分数。

虽然规范对于评分很有用，但也需要相当多的磁盘(通常按照索引中每个字段每个文档一个字节的顺序排列，即使对于没有此特定字段的文档也是如此)。因此，如果您不需要在特定字段上评分，则应禁用该字段的规范。特别是，仅用于筛选或聚合的字段就是这种情况。

可以使用更新映射 API 在现有字段上禁用规范。

可以使用更新映射 API 禁用规范(但事后不会重新启用)，如下所示：

    
    
    response = client.indices.put_mapping(
      index: 'my-index-000001',
      body: {
        properties: {
          title: {
            type: 'text',
            norms: false
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_mapping
    {
      "properties": {
        "title": {
          "type": "text",
          "norms": false
        }
      }
    }

规范不会立即删除，但会在您继续为新文档编制索引时将旧段合并为新段时删除。在已删除规范的字段上进行的任何 scorecomputing 都可能返回不一致的结果，因为某些文档将不再具有规范，而其他文档可能仍具有规范。

[« `normalizer`](normalizer.md) [`null_value` »](null-value.md)



[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md) ›[Mapping parameters](mapping-params.md)

[« `dynamic`](dynamic.md) [`enabled` »](enabled.md)

##'eager_global_ordinals'

### 什么是全局序数？

为了支持聚合和其他需要在每个文档上查找字段值的操作，Elasticsearch 使用了一种名为 eddoc values 的数据结构。基于术语的字段类型(如"关键字")使用序号映射存储其文档值，以实现更紧凑的表示形式。此映射的工作原理是根据每个术语的词典顺序为每个术语分配一个增量整数或 _序号_。字段的文档值仅存储每个文档的序号，而不是原始术语，并使用单独的查找结构在序号和术语之间进行转换。

在聚合期间使用时，序数可以大大提高性能。例如，"terms"聚合仅依赖于序号将文档收集到分片级别的存储桶中，然后在跨分片组合结果时将序数转换回其原始术语值。

每个索引段定义自己的序号映射，但聚合跨整个分片收集数据。因此，为了能够将序数用于聚合等分片级操作，Elasticsearch 创建了一个统一的映射called_global ordinals_。全局序号映射建立在分段序数之上，并通过维护每个段从全局序号到局部序号的映射来工作。

如果搜索包含以下任何组件，则使用全局序号：

* "关键字"、"ip"和"扁平化"字段上的某些存储桶聚合。这包括上述"术语"聚合，以及"复合"、"diversified_sampler"和"significant_terms"。  * 需要启用"字段数据"的"文本"字段上的存储桶聚合。  * 对"联接"字段中的父文档和子文档的操作，包括"has_child"查询和"父"聚合。

全局序号映射使用堆内存作为字段数据缓存的一部分。高基数字段上的聚合可能会使用大量内存并触发字段数据断路器。

### 加载全局序数

必须先构建全局序号映射，然后才能在搜索期间使用序号。默认情况下，映射在搜索期间首次需要全局序号时加载。如果要优化索引速度，这是正确的方法，但如果搜索性能是优先事项，建议在将在聚合中使用的字段上急切地加载全局序号：

    
    
    response = client.indices.put_mapping(
      index: 'my-index-000001',
      body: {
        properties: {
          tags: {
            type: 'keyword',
            eager_global_ordinals: true
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_mapping
    {
      "properties": {
        "tags": {
          "type": "keyword",
          "eager_global_ordinals": true
        }
      }
    }

启用"eager_global_ordinals"后，会在刷新 ashard 时构建全局序号——Elasticsearch 总是在公开对索引内容的更改之前加载它们。这会将构建全局序号的成本从搜索转移到索引时。Elasticsearch 在创建分片的新副本时也会急切地构建全局序数，就像增加副本数量或将分片重新定位到新节点时一样。

可以随时通过更新"eager_global_ordinals"设置来禁用预先加载：

    
    
    response = client.indices.put_mapping(
      index: 'my-index-000001',
      body: {
        properties: {
          tags: {
            type: 'keyword',
            eager_global_ordinals: false
          }
        }
      }
    )
    puts response
    
    
    PUT my-index-000001/_mapping
    {
      "properties": {
        "tags": {
          "type": "keyword",
          "eager_global_ordinals": false
        }
      }
    }

### 避免全局序号加载

通常，全局序数在加载时间和内存使用方面不会产生很大的开销。但是，在具有大型分片的索引上加载全局序数可能会很昂贵，或者如果字段包含大量唯一术语值。由于全局序数为分片上的所有段提供了统一的映射，因此当新段可见时，还需要完全重建它们。

在某些情况下，可以完全避免全局序号加载：

* "术语"、"采样器"和"significant_terms"聚合支持参数"execution_hint"，该参数有助于控制存储桶的收集方式。它默认为"global_ordinals"，但可以设置为"map"以直接使用术语值。  * 如果一个分片被强制合并到单个段，那么它的段序数已经_全局_到分片。在这种情况下，Elasticsearch 不需要构建全局序号映射，使用全局序号也不会产生额外的开销。请注意，出于性能原因，您应该只强制合并永远不会再次写入的索引。

[« `dynamic`](dynamic.md) [`enabled` »](enabled.md)

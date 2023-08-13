

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Index
modules](index-modules.md) ›[Store](index-modules-store.md)

[« Store](index-modules-store.md) [Translog »](index-modules-translog.md)

## 将数据预加载到文件系统缓存中

这是一个专家设置，其细节将来可能会发生变化。

默认情况下，Elasticsearch 完全依赖于操作系统文件系统缓存来缓存 I/O 操作。可以设置"index.store.preload"，以便告诉操作系统在打开时将热索引文件的内容加载到内存中。此设置接受逗号分隔的文件扩展名列表：扩展名在列表中的所有文件将在打开时预加载。这对于提高索引的搜索性能非常有用，尤其是在重新启动主机操作系统时，因为这会导致文件系统缓存被丢弃。但请注意，这可能会减慢索引的打开速度，因为它们只有在数据加载到物理内存后才可用。

此设置仅尽力而为，可能根本不起作用，具体取决于商店类型和主机操作系统。

"index.store.preload"是一个静态设置，可以在"config/elasticsearch.yml"中设置：

    
    
    index.store.preload: ["nvd", "dvd"]

或在创建索引时的索引设置中：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          "index.store.preload": [
            'nvd',
            'dvd'
          ]
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001
    {
      "settings": {
        "index.store.preload": ["nvd", "dvd"]
      }
    }

默认值为空数组，这意味着不会急切地将任何内容加载到文件系统缓存中。对于主动搜索的索引，您可能希望将其设置为"["nvd"，"dvd"]"，这将导致规范和文档值急切地加载到物理内存中。这是两个首先要看的扩展，因为Elasticsearch对它们执行随机访问。

可以使用通配符来指示所有文件都应预加载："index.store.preload： ["*"]"。但请注意，将所有文件加载到内存中通常没有用，特别是存储字段和术语向量的文件，因此更好的选择可能是将其设置为"["nvd"、"dvd"、"tim"、"doc"、"dim"]"，这将预加载规范、文档值、术语词典、帖子列表和点，这是搜索和聚合索引中最重要的部分。

对于矢量搜索，您使用近似 k 最近邻搜索，您可能希望将设置设置为矢量搜索文件："["vec"、"vex"、"vem"]"("vec"用于矢量值，"vex" – 用于 HNSW 图，"vem" – 用于元数据)。

请注意，此设置在大于主机主内存大小的索引上可能很危险，因为它会导致文件系统缓存在大型合并后重新打开时被丢弃，这将使索引和搜索_变慢_。

[« Store](index-modules-store.md) [Translog »](index-modules-translog.md)

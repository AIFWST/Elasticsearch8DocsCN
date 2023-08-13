

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Index
modules](index-modules.md) ›[Index Shard Allocation](index-modules-
allocation.md)

[« Delaying allocation when a node leaves](delayed-allocation.md) [Total
shards per node »](allocation-total-shards.md)

## 索引恢复优先级

未分配的分片将尽可能按优先级顺序恢复。索引按优先级顺序排序如下：

* 可选的"索引优先级"设置(先高后低) * 索引创建日期(先高后低) * 索引名称(先高后低)

这意味着，默认情况下，较新的索引将在较旧的索引之前恢复。

使用每个索引可动态更新的"index.priority"设置来自定义索引优先级顺序。例如：

    
    
    response = client.indices.create(
      index: 'index_1'
    )
    puts response
    
    response = client.indices.create(
      index: 'index_2'
    )
    puts response
    
    response = client.indices.create(
      index: 'index_3',
      body: {
        settings: {
          "index.priority": 10
        }
      }
    )
    puts response
    
    response = client.indices.create(
      index: 'index_4',
      body: {
        settings: {
          "index.priority": 5
        }
      }
    )
    puts response
    
    
    PUT index_1
    
    PUT index_2
    
    PUT index_3
    {
      "settings": {
        "index.priority": 10
      }
    }
    
    PUT index_4
    {
      "settings": {
        "index.priority": 5
      }
    }

在上面的例子中：

* "index_3"将首先恢复，因为它具有最高的"index.priority"。  * 接下来将恢复"index_4"，因为它具有下一个最高优先级。  * 接下来将恢复"index_2"，因为它是最近创建的。  * "index_1"将最后恢复。

此设置接受整数，可以使用更新索引设置 API 在实时索引上更新：

    
    
    response = client.indices.put_settings(
      index: 'index_4',
      body: {
        "index.priority": 1
      }
    )
    puts response
    
    
    PUT index_4/_settings
    {
      "index.priority": 1
    }

[« Delaying allocation when a node leaves](delayed-allocation.md) [Total
shards per node »](allocation-total-shards.md)

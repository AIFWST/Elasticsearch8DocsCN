

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authorization](authorization.md)

[« Field level security](field-level-security.md) [Mapping users and groups
to roles »](mapping-roles.md)

## 授予数据流和别名的权限

Elasticsearch 安全功能允许您保护针对数据流和别名执行的操作。

### 数据流特权

使用索引权限控制对数据流的访问。授予权限 数据流对其后备索引授予相同的权限。

例如，"my-data-stream"由两个支持索引组成：".ds-my-data-stream-2099.03.07-000001"和".ds-my-data-stream-2099.03.08-000002"。

用户被授予对"我的数据流"的"读取"权限。

    
    
    {
      "names" : [ "my-data-stream" ],
      "privileges" : [ "read" ]
    }

由于用户被自动授予对流的支持索引的相同权限，因此用户可以直接从".ds-my-data-stream-2099.03.08-000002"检索文档：

    
    
    response = client.get(
      index: '.ds-my-data-stream-2099.03.08-000002',
      id: 2
    )
    puts response
    
    
    GET .ds-my-data-stream-2099.03.08-000002/_doc/2

后来"我的数据流"滚动。这将创建一个新的支持索引：".ds-my-data-stream-2099.03.09-000003"。由于用户仍具有"my-data-stream"的"读取"权限，因此用户可以直接从".ds-my-data-stream-2099.03.09-000003"检索文档：

    
    
    response = client.get(
      index: '.ds-my-data-stream-2099.03.09-000003',
      id: 2
    )
    puts response
    
    
    GET .ds-my-data-stream-2099.03.09-000003/_doc/2

### 别名权限

使用索引权限控制对别名的访问。对索引或数据流的权限不会授予对其别名的权限。有关管理别名的信息，请参阅 _别名_。

不要使用筛选的别名来代替文档级安全性。Elasticsearch 并不总是应用别名过滤器。

例如，"current_year"别名仅指向"2015"索引。用户被授予"2015"索引的"读取"权限。

    
    
    {
      "names" : [ "2015" ],
      "privileges" : [ "read" ]
    }

当用户尝试从"current_year"别名中检索文档时，Elasticsearch 会拒绝该请求。

    
    
    response = client.get(
      index: 'current_year',
      id: 1
    )
    puts response
    
    
    GET current_year/_doc/1

要从"current_year"检索文档，用户必须具有别名的"读取"索引权限。

    
    
    {
      "names" : [ "current_year" ],
      "privileges" : [ "read" ]
    }

[« Field level security](field-level-security.md) [Mapping users and groups
to roles »](mapping-roles.md)



[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md)

[« Watcher chain payload transform](transform-chain.md) [Example watches
»](example-watches.md)

## 管理手表

观察程序提供了一组可用于管理监视的 API：

* 使用创建或更新监视 API 添加或更新监视 * 使用获取监视 API 检索监视 * 使用删除监视 API 删除监视 * 使用激活监视 API 激活监视 * 使用停用监视 API 停用监视 * 使用确认监视 API 确认监视

### 列表监视

目前没有用于列出存储手表的专用 API。但是，由于 Watcher 将其监视存储在".watches"索引中，因此您可以通过在此索引上执行搜索来列出它们。

您只能对".watches"索引执行读取操作。必须使用观察程序 API 来创建、更新和删除监视。如果启用了 Elasticsearch 安全功能，我们建议您只授予用户对 '.watches' 索引的"读取"权限。

例如，以下内容返回前 100 个监视：

    
    
    GET /_watcher/_query/watches
    {
      "size" : 100
    }

[« Watcher chain payload transform](transform-chain.md) [Example watches
»](example-watches.md)

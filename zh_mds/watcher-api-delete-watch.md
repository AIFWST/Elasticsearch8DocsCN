

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Watcher APIs](watcher-api.md)

[« Deactivate watch API](watcher-api-deactivate-watch.md) [Execute watch API
»](watcher-api-execute-watch.md)

## 删除监视接口

从观察器中删除监视。

###Request

"删除_watcher/监视/<watch_id>"

###Prerequisites

* 您必须具有"manage_watcher"群集权限才能使用此 API。有关详细信息，请参阅安全权限。

###Description

删除监视时，在".watches"索引中表示监视的文档将消失，并且永远不会再次运行。

请注意，删除手表**不会**从手表历史记录中删除与此手表相关的任何手表执行记录。

删除监视只能通过此 API 完成。不要使用 Elasticsearch DELETE DocumentAPI 直接从 '.watches' 索引中删除监视。启用 Elasticsearch 安全功能后，请确保没有通过".watches"索引向任何人授予"写入"权限。

### 路径参数

`<watch_id>`

     (Required, string) Identifier for the watch. 

###Examples

以下示例删除具有"my-watch"ID 的手表：

    
    
    response = client.watcher.delete_watch(
      id: 'my_watch'
    )
    puts response
    
    
    DELETE _watcher/watch/my_watch

Response:

    
    
    {
       "found": true,
       "_id": "my_watch",
       "_version": 2
    }

[« Deactivate watch API](watcher-api-deactivate-watch.md) [Execute watch API
»](watcher-api-execute-watch.md)
